CREATE TABLE dwd_zrr_dzyx_new (
    zrrwybs VARCHAR(800),
    yxzh VARCHAR(800),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800)
);

COMMENT ON TABLE dwd_zrr_dzyx_new IS '电子邮箱';
COMMENT ON COLUMN dwd_zrr_dzyx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_dzyx_new.yxzh IS '邮箱账号';
COMMENT ON COLUMN dwd_zrr_dzyx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_dzyx_new.sfzjhm IS '身份证件号码';