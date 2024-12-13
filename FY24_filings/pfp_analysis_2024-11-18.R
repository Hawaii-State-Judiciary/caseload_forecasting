
# load packages -----------------------------------------------------------
library(readxl)
library(dplyr)


# import data -------------------------------------------------------------

pfp <- read_excel("pfp_extract_2024-12-13_0917.xlsx")

filings <- pfp %>% 
  mutate(CASE_TYPE_recode = case_when(CASE_TYPE %in% c("TC","TI","TP") ~ "traffic_filings", 
                                      CASE_TYPE == "CV" ~ "civil_action_filings",
                                      CASE_TYPE == "PC" ~ "criminal_action_filings",
                                      CASE_TYPE == "DV" ~ "marital_action_filings",
                                      CASE_TYPE == "AN" ~ "adoption_filings",
                                      CASE_TYPE == "PA" ~ "paternity_filings"
                                      ),
         case_type = factor(CASE_TYPE_recode, levels = c("civil_action_filings","criminal_action_filings", 
                                                         "marital_action_filings", "adoption_filings", 
                                                         "paternity_filings", "traffic_filings"))) %>% 
  count(circuit = COURT, case_type, name = "frequency (n)")

write.csv(filings, paste0("pfp_results_", Sys.Date(),".csv"), row.names = F)
