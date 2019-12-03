"""
Pseudocode
BEGIN 
    INITIALISE population
    REPEAT UNTIL (termination condition IS satisfied) DO
        UPDATE global best
        FOR EACH (particle IN population) DO
            1. UPDATE velocity AND position
            2. EVALUATE new position
            3. UPDATE personal best
        OD
    OD
END
"""
