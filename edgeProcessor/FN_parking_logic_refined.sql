-- FUNCTION: public.parking_logic_refined(character varying, character varying)

-- DROP FUNCTION IF EXISTS public.parking_logic_refined(character varying, character varying);

CREATE OR REPLACE FUNCTION public.parking_logic_refined(
	p_car_plate_num character varying,
	p_parkinglot_addr character varying,
	OUT result text)
    RETURNS text
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    query_time TIMESTAMP (0) WITH TIME ZONE = CURRENT_TIMESTAMP(0);
    last_arrival_time TIMESTAMP (0) WITH TIME ZONE;
    last_departure_time TIMESTAMP (0) WITH TIME ZONE;
    is_parking_in BOOLEAN = FALSE;
    per_hour_fee NUMERIC(8,2);
    v_parking_fee NUMERIC(8,2);
    v_max_due NUMERIC(8,2);
    v_user_due NUMERIC(8,2);
    v_user_id BIGINT;
    v_pl_id BIGINT;
    v_car_id BIGINT;
    has_spot BOOLEAN;
BEGIN
    result = 'INITIAL';
    
    -- get required values
    SELECT cc.id, owner_id, in_time, out_time
    INTO v_car_id, v_user_id, last_arrival_time, last_departure_time
    FROM customers_car cc
    WHERE license_plate_number = p_car_plate_num;
    
    SELECT ap.id, fee_per_hour, max_overdue
    INTO v_pl_id, per_hour_fee, v_max_due
    FROM administrators_parkinglot ap
    WHERE street_address = p_parkinglot_addr;
    
    -- first check if associated user exist 
    IF v_user_id IS NULL THEN
        result = 'Not Registered';
        RETURN;
    END IF;
    
    -- second check direction
    IF last_arrival_time IS NULL THEN
        is_parking_in = TRUE;
    ELSEIF last_departure_time IS NULL THEN
        is_parking_in = FALSE;
    ELSE
        is_parking_in = (last_departure_time >= last_arrival_time);
    END IF;
    
    IF is_parking_in THEN
        -- if parking in
        v_user_due = (SELECT balance_due FROM users_user uu WHERE uu.id = v_user_id);
        -- check overdue
        IF v_max_due < v_user_due THEN
            result = 'Too Much Overdue';
            RETURN;
        END IF;
        -- check spots left
        has_spot = 
            (SELECT free_spots 
                FROM administrators_parkinglot ap
                WHERE ap.id = v_pl_id) > 0;
                
        IF NOT has_spot THEN
            result = 'Parkinglot Full';
            RETURN;
        END IF;
        -- update car status    
        UPDATE customers_car cc
            SET in_time = query_time, parking_id = v_pl_id
            WHERE cc.id = v_car_id;
        -- update free spots
        UPDATE administrators_parkinglot ap
            SET free_spots = free_spots - 1
            WHERE ap.id = v_pl_id;
        
        result = 'Successfully Parked In';
        RETURN;    
    ELSE
        -- if parking out
        -- update car status
        UPDATE customers_car cc
            SET out_time = query_time
            WHERE cc.id = v_car_id;
        
        -- https://www.postgresql.org/message-id/20071125085321.GA20882@KanotixBox 
        v_parking_fee = 
            (SELECT EXTRACT(EPOCH FROM query_time - last_arrival_time)/3600) * per_hour_fee;
        
        -- update free spots
        UPDATE administrators_parkinglot ap
            SET free_spots = free_spots + 1
            WHERE ap.id = v_pl_id;
        
        -- insert history
        INSERT INTO customers_parkinghistory (car_id, parking_id, in_time, out_time, parking_fee, paid, payment_date)
            VALUES (v_car_id, v_pl_id, last_arrival_time, query_time, v_parking_fee, FALSE, query_time);
        
        -- update balance
        UPDATE users_user uu
            SET balance_due = balance_due + v_parking_fee
            WHERE uu.id = v_user_id;
        
        result = 'Successfully Parked Out';
        RETURN;
    END IF;
END;
$BODY$;

ALTER FUNCTION public.parking_logic_refined(character varying, character varying)
    OWNER TO isgpdqkheqripx;
