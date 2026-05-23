CREATE TABLE dwd_zrr_zccz_new (
    zrrwybs VARCHAR(800),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    dyw VARCHAR(2040),
    dyzt VARCHAR(2040),
    dyqxq DATE,
    dyqxz DATE,
    dyqzxdjsj DATE
);

COMMENT ON TABLE dwd_zrr_zccz_new IS '资产处置';
COMMENT ON COLUMN dwd_zrr_zccz_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_zccz_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_zccz_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_zccz_new.dyw IS '抵押物';
COMMENT ON COLUMN dwd_zrr_zccz_new.dyzt IS '抵押状态';
COMMENT ON COLUMN dwd_zrr_zccz_new.dyqxq IS '抵押期限起';
COMMENT ON COLUMN dwd_zrr_zccz_new.dyqxz IS '抵押期限止';
COMMENT ON COLUMN dwd_zrr_zccz_new.dyqzxdjsj IS '抵押权注销登记时间';