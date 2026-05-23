CREATE TABLE dwd_zrr_ycxx_new (
    zrrwybs VARCHAR(200),
    sfzjlx CHAR(50),
    sfzjhm VARCHAR(200),
    ycbm VARCHAR(255),
    cjg VARCHAR(255),
    cm VARCHAR(255),
    ycdjzsbh VARCHAR(255)
);

COMMENT ON TABLE dwd_zrr_ycxx_new IS '渔船信息';
COMMENT ON COLUMN dwd_zrr_ycxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_ycxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_ycxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_ycxx_new.ycbm IS '渔船编码';
COMMENT ON COLUMN dwd_zrr_ycxx_new.cjg IS '船舶港';
COMMENT ON COLUMN dwd_zrr_ycxx_new.cm IS '船名';
COMMENT ON COLUMN dwd_zrr_ycxx_new.ycdjzsbh IS '渔船登记证书编号';