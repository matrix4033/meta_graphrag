CREATE TABLE dwd_zrr_yzwl_new (
    zrrwybs VARCHAR(800),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    jjrxm VARCHAR(800)
);

COMMENT ON TABLE dwd_zrr_yzwl_new IS '邮政物流新';
COMMENT ON COLUMN dwd_zrr_yzwl_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_yzwl_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_yzwl_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_yzwl_new.jjrxm IS '寄件人姓名';