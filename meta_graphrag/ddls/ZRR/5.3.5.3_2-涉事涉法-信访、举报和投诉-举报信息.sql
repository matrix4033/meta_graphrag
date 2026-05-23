CREATE TABLE dwd_zrr_jbxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    xxlb CHAR(8),
    gjzms VARCHAR(4000),
    wtlb CHAR(48),
    jtwt VARCHAR(16000)
);

COMMENT ON TABLE dwd_zrr_jbxx_new IS '举报信息';
COMMENT ON COLUMN dwd_zrr_jbxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_jbxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_jbxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_jbxx_new.xxlb IS '信息类别';
COMMENT ON COLUMN dwd_zrr_jbxx_new.gjzms IS '关键字描述';
COMMENT ON COLUMN dwd_zrr_jbxx_new.wtlb IS '问题类别';
COMMENT ON COLUMN dwd_zrr_jbxx_new.jtwt IS '具体问题';