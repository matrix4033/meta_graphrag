CREATE TABLE dwd_zrr_lxdh_new (
    zrrwybs VARCHAR(200),
    sfzjlx CHAR(50),
    sfzjhm VARCHAR(200),
    dhhm VARCHAR(100)
);

COMMENT ON TABLE dwd_zrr_lxdh_new IS '联系电话';
COMMENT ON COLUMN dwd_zrr_lxdh_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_lxdh_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_lxdh_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_lxdh_new.dhhm IS '电话号码';