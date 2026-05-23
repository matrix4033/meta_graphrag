CREATE TABLE dwd_zrr_cbxx_new (
    zrrwybs VARCHAR(800),
    sfzjhm VARCHAR(800),
    sfzjlx CHAR(16),
    cmzw VARCHAR(2040),
    cmyw VARCHAR(2040),
    ch VARCHAR(2040),
    cjgzw VARCHAR(2040),
    cjgyw VARCHAR(2040),
    czdw VARCHAR(2040),
    cbsyqzh VARCHAR(2040),
    cbzsh VARCHAR(2040),
    cmdm VARCHAR(2040),
    cz VARCHAR(2040)
);

COMMENT ON TABLE dwd_zrr_cbxx_new IS '船舶信息表';
COMMENT ON COLUMN dwd_zrr_cbxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_cbxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_cbxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_cbxx_new.cmzw IS '船名(中文)';
COMMENT ON COLUMN dwd_zrr_cbxx_new.cmyw IS '船名(英文)';
COMMENT ON COLUMN dwd_zrr_cbxx_new.ch IS '船号';
COMMENT ON COLUMN dwd_zrr_cbxx_new.cjgzw IS '船籍港(中文)';
COMMENT ON COLUMN dwd_zrr_cbxx_new.cjgyw IS '船籍港(英文)';
COMMENT ON COLUMN dwd_zrr_cbxx_new.czdw IS '船总吨位';
COMMENT ON COLUMN dwd_zrr_cbxx_new.cbsyqzh IS '船舶所有权证号';
COMMENT ON COLUMN dwd_zrr_cbxx_new.cbzsh IS '船舶证书号';
COMMENT ON COLUMN dwd_zrr_cbxx_new.cmdm IS '船名代码';
COMMENT ON COLUMN dwd_zrr_cbxx_new.cz IS '船质';