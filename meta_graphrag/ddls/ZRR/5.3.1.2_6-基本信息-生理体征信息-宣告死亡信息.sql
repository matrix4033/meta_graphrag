CREATE TABLE dwd_zrr_xgswxx_new (
    zrrwybs VARCHAR(800),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    sxpjrq DATE,
    jarg DATE,
    ah VARCHAR(64)
);

COMMENT ON TABLE dwd_zrr_xgswxx_new IS '宣告死亡信息';
COMMENT ON COLUMN dwd_zrr_xgswxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_xgswxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_xgswxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_xgswxx_new.sxpjrq IS '死刑判决日期';
COMMENT ON COLUMN dwd_zrr_xgswxx_new.jarg IS '结案日期';
COMMENT ON COLUMN dwd_zrr_xgswxx_new.ah IS '案号';