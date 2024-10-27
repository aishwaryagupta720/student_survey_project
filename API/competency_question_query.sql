 SELECT 
            'communication' AS competency,
            elements->>'order' AS question_order,
            array_agg(elements->>'score_value') AS score_values
        FROM 
            student_response sr,
            jsonb_array_elements(sr.communication) AS elements
        
    WHERE
        1=1
     AND sr.inventory_version = %s AND sr.semester = %s AND sr.org_name = %s AND sr.implementation_type = %s 
        GROUP BY question_order
             UNION ALL 
        SELECT 
            'teamwork' AS competency,
            elements->>'order' AS question_order,
            array_agg(elements->>'score_value') AS score_values
        FROM 
            student_response sr,
            jsonb_array_elements(sr.teamwork) AS elements
        
    WHERE
        1=1
     AND sr.inventory_version = %s AND sr.semester = %s AND sr.org_name = %s AND sr.implementation_type = %s 
        GROUP BY question_order
             UNION ALL 
        SELECT 
            'self_development' AS competency,
            elements->>'order' AS question_order,
            array_agg(elements->>'score_value') AS score_values
        FROM 
            student_response sr,
            jsonb_array_elements(sr.self_development) AS elements
        
    WHERE
        1=1
     AND sr.inventory_version = %s AND sr.semester = %s AND sr.org_name = %s AND sr.implementation_type = %s 
        GROUP BY question_order
             UNION ALL 
        SELECT 
            'professionalism' AS competency,
            elements->>'order' AS question_order,
            array_agg(elements->>'score_value') AS score_values
        FROM 
            student_response sr,
            jsonb_array_elements(sr.professionalism) AS elements
        
    WHERE
        1=1
     AND sr.inventory_version = %s AND sr.semester = %s AND sr.org_name = %s AND sr.implementation_type = %s 
        GROUP BY question_order
             UNION ALL 
        SELECT 
            'leadership' AS competency,
            elements->>'order' AS question_order,
            array_agg(elements->>'score_value') AS score_values
        FROM 
            student_response sr,
            jsonb_array_elements(sr.leadership) AS elements
        
    WHERE
        1=1
     AND sr.inventory_version = %s AND sr.semester = %s AND sr.org_name = %s AND sr.implementation_type = %s 
        GROUP BY question_order
             UNION ALL 
        SELECT 
            'critical_thinking' AS competency,
            elements->>'order' AS question_order,
            array_agg(elements->>'score_value') AS score_values
        FROM 
            student_response sr,
            jsonb_array_elements(sr.critical_thinking) AS elements
        
    WHERE
        1=1
     AND sr.inventory_version = %s AND sr.semester = %s AND sr.org_name = %s AND sr.implementation_type = %s 
        GROUP BY question_order
             UNION ALL 
        SELECT 
            'technology' AS competency,
            elements->>'order' AS question_order,
            array_agg(elements->>'score_value') AS score_values
        FROM 
            student_response sr,
            jsonb_array_elements(sr.technology) AS elements
        
    WHERE
        1=1
     AND sr.inventory_version = %s AND sr.semester = %s AND sr.org_name = %s AND sr.implementation_type = %s 
        GROUP BY question_order
             UNION ALL 
        SELECT 
            'equity' AS competency,
            elements->>'order' AS question_order,
            array_agg(elements->>'score_value') AS score_values
        FROM 
            student_response sr,
            jsonb_array_elements(sr.equity) AS elements
        
    WHERE
        1=1
     AND sr.inventory_version = %s AND sr.semester = %s AND sr.org_name = %s AND sr.implementation_type = %s 
        GROUP BY question_order
            ORDER BY question_order