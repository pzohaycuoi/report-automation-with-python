-- 🔥 Table: ea_report_date
CREATE TABLE db_billing_report.ea_report_date
(
  date varchar(8) NOT NULL,
  day int,
  month int,
  year int,
  quarter int,
  day_of_week int,
  day_name varchar(9),
  month_name varchar(9),
  CONSTRAINT PK_ea_report_date PRIMARY KEY (date)
);

-- 🔥 Table: ea_accounts
CREATE TABLE db_billing_report.ea_accounts
(
  enrollment_number int NOT NULL,
  account_status varchar(50),
  start_date varchar(8),
  end_date varchar(8),
  company_name varchar(200),
  country varchar(5),
  billing_cycle varchar(20),
  CONSTRAINT PK_ea_accounts PRIMARY KEY (enrollment_number)
);

-- 🔥 Table: ea_account_synced_date
CREATE TABLE db_billing_report.ea_account_synced_date
(
  enrollment_number int NOT NULL,
  date varchar(8) NOT NULL,
  day int,
  month int,
  year int,
  CONSTRAINT PK_ea_account_synced_date PRIMARY KEY (enrollment_number, date),
  CONSTRAINT FK_ea_account_synced_date_ea_accounts FOREIGN KEY (enrollment_number)
    REFERENCES db_billing_report.ea_accounts (enrollment_number)
);

-- 🔥 Table: ea_balance_summaries
CREATE TABLE db_billing_report.ea_balance_summaries
(
  enrollment_number int NOT NULL,
  date varchar(8) NOT NULL,
  currency varchar(10),
  beginning_balance numeric(10, 2),
  ending_balance numeric(10, 2),
  new_purchases numeric(10, 2),
  adjustments numeric(10, 2),
  utilized numeric(10, 2),
  service_overage numeric(10, 2),
  charges_billed_separately numeric(10, 2),
  total_overage numeric(10, 2),
  total_usage numeric(10, 4),
  azure_marketplace_service_charges numeric(10, 10),
  billing_frequency varchar(20),
  price_hidden bit,
  CONSTRAINT PK_ea_balance_summaries PRIMARY KEY (enrollment_number, date),
  CONSTRAINT FK_ea_balance_summaries_ea_report_date FOREIGN KEY (date)
    REFERENCES db_billing_report.ea_report_date (date) 
);

-- 🔥 Table: ea_ri_charges
CREATE TABLE db_billing_report.ea_ri_charges
(
  reservation_order_name varchar(40) NOT NULL,
  enrollment_number int NOT NULL,
  date varchar(8) NOT NULL,
  arm_sku_name varchar(50),
  term varchar(20),
  region varchar(20),
  purchasing_subscription_guid varchar(50),
  purchasing_subscription_name varchar(100),
  account_name varchar(50),
  account_owner_email varchar(50),
  cost_center varchar(50),
  event_date varchar(30),
  reservation_order_id varchar(50),
  description varchar(100),
  event_type varchar(20),
  quantity numeric(10, 2),
  amount numeric(10, 2),
  currency varchar(10),
  billing_frequency varchar(20),
  CONSTRAINT PK_ea_ri_charges PRIMARY KEY (reservation_order_name, enrollment_number, date),
  CONSTRAINT FK_ea_ri_charges_ea_report_date FOREIGN KEY (date)
    REFERENCES db_billing_report.ea_report_date (date),
  CONSTRAINT FK_ea_ri_charges_ea_accounts FOREIGN KEY (enrollment_number)
    REFERENCES db_billing_report.ea_accounts (enrollment_number)
);

-- 🔥 Table: ea_price_sheet
CREATE TABLE db_billing_report.ea_price_sheet
(
  enrollment_number int NOT NULL,
  date varchar(8) NOT NULL,
  meter_id varchar(50) NOT NULL,
  billing_period_id int,
  unit_of_measure varchar(50),
  included_quantity numeric(10, 2),
  part_number varchar(20),
  unit_price numeric(10, 2),
  currency_code varchar(10),
  offer_id varchar(50),
  meter_name varchar(50),
  meter_category varchar(50),
  unit varchar(20),
  meter_location varchar(max),
  total_included_quantity numeric(15, 15),
  pretax_standard_rate numeric(15, 15),
  CONSTRAINT PK_ea_price_sheet PRIMARY KEY (enrollment_number, date, meter_id),
  CONSTRAINT FK_ea_price_sheet_ea_report_date FOREIGN KEY (date)
    REFERENCES db_billing_report.ea_report_date (date),
  CONSTRAINT FK_ea_price_sheet_ea_accounts FOREIGN KEY (enrollment_number)
    REFERENCES db_billing_report.ea_accounts (enrollment_number)
);

-- 🔥 Table: ea_detail_usage
CREATE TABLE db_billing_report.ea_detail_usage
(
  enrollment_number int NOT NULL,
  date varchar(8) NOT NULL,
  meter_id varchar(50) NOT NULL,
  is_azure_credit_eligible bit,
  cost numeric(15, 15),
  consumed_service varchar(30),
  invoice_section varchar(50),
  account_owner_id varchar(50),
  account_name varchar(50),
  subscription_id varchar(50),
  subscription_name varchar(50),
  quantity numeric(15, 15),
  effective_price numeric(15, 15),
  resource_location varchar(20),
  resource_id varchar(300),
  service_info_1 varchar(100),
  service_info_2 varchar(100),
  cost_center varchar(100),
  resource_group varchar(50),
  plan_name varchar(100),
  publisher_name varchar(100),
  tags nvarchar(max),
  additional_info nvarchar(max),
  CONSTRAINT PK_ea_detail_usage PRIMARY KEY (enrollment_number, date, meter_id),
  CONSTRAINT FK_ea_detail_usage_ea_report_date FOREIGN KEY (date)
    REFERENCES db_billing_report.ea_report_date (date),
  CONSTRAINT FK_ea_detail_usage_ea_accounts FOREIGN KEY (enrollment_number)
    REFERENCES db_billing_report.ea_accounts (enrollment_number),
  -- CONSTRAINT FK_ea_detail_usage_ea_price_sheet FOREIGN KEY (meter_id)
  --   REFERENCES db_billing_report.ea_price_sheet (meter_id)
);
