
# load packages -----------------------------------------------------------
library(readxl)
library(dplyr)


# import data -------------------------------------------------------------

pfp <- read_excel("pfp_extract_2024-11-18_1401.xlsx")

filings_circuit <- pfp %>% 
  mutate(CASE_TYPE_recode = case_when(CASE_TYPE %in% c("TC","TI","TP") ~ "traffic_filings", 
                                      CASE_TYPE == "CV" ~ "civil_action_filings",
                                      CASE_TYPE == "PC" ~ "criminal_action_filings",
                                      CASE_TYPE == "DV" ~ "marital_action_filings"),
         CASE_TYPE_recode = factor(CASE_TYPE_recode, levels = c("civil_action_filings","criminal_action_filings", 
                                                                 "marital_action_filings", "traffic_filings"))) %>% 
  count(COURT, CASE_TYPE_recode, name = "frequency (n)")
