-- 创建临时表

DROP TABLE pc_temp_result;

CREATE GLOBAL TEMPORARY TABLE pc_temp_result (

   p_name VARCHAR2(100),

   c_date VARCHAR2(100),

   manager VARCHAR2(100),

   p_totalnav NUMBER,

   p_rtn_y NUMBER,

   pre_m NUMBER,

   pre_w NUMBER,

   RK VARCHAR2(100)

) ON COMMIT PRESERVE ROWS; --DELETE


DECLARE

    output_cursor SYS_REFCURSOR; -- 声明游标变量


BEGIN

    -- 调用存储过程并传入参数值，并将结果赋给游标变量

   PKG_REP_AUTO.PROC_NJ_REP_V(P_RETURNS => output_cursor,

                               P_TDATE => '2023-06-29',

                               P_FLAG => '4',

                               P_TYPE => '1');


    -- 将结果插入到临时表中

    FOR rec IN (SELECT p_name, c_date, manager, p_totalnav,

                        p_rtn_y, pre_m, pre_w, RK FROM TABLE(output_cursor))

    LOOP

    INSERT INTO pc_temp_result VALUES (rec.p_name, rec.c_date, rec.manager,

                                   rec.p_totalnav, rec.p_rtn_y,

                                   rec.pre_m, rec.pre_w, rec.RK);  

     

      /*可在此处执行其他操作*/

     

   END LOOP;

   

END;