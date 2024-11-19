--FY24
WITH 
constFY AS ( SELECT 
    '01-JUL-2023' AS startFY, --use with BETWEEN
    '30-JUN-2024'  AS endFY, --use with BETWEEN
    '01-JUL-2024' AS newFY --use as cutoff
    FROM DUAL
)

--Filings with case status
SELECT CDBCASE_ID CASE_ID, 
  CDBCASE_CORT_CODE COURT, 
  CDBCASE_CTYP_CODE CASE_TYPE, 
  CDBCASE_LOCN_CODE LOC, 
  CDBCASE_INIT_FILING INIT_DATE
FROM (SELECT * 
        FROM CDBCASE,constFY 
        WHERE CDBCASE_INIT_FILING  BETWEEN startFY AND endFY
        AND CDBCASE_CTYP_CODE in ('PC','CV','DV','TC','TI','TP'))