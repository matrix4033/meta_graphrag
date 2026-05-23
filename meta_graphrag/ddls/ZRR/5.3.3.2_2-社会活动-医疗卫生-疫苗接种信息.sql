CREATE TABLE dwd_zrr_ymjzxx_new (
    zrrwybs VARCHAR(800),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    ymbm VARCHAR(500),
    jzlx VARCHAR(500),
    ymxh VARCHAR(500),
    scqy VARCHAR(2000),
    jzrq VARCHAR(500),
    jzbw VARCHAR(500),
    jzys VARCHAR(500),
    jzjgbm VARCHAR(500),
    fybz VARCHAR(500)
);

COMMENT ON TABLE dwd_zrr_ymjzxx_new IS '疫苗接种信息';
COMMENT ON COLUMN dwd_zrr_ymjzxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_ymjzxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_ymjzxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_ymjzxx_new.ymbm IS '疫苗编码';
COMMENT ON COLUMN dwd_zrr_ymjzxx_new.jzlx IS '接种类型';
COMMENT ON COLUMN dwd_zrr_ymjzxx_new.ymxh IS '疫苗序号';
COMMENT ON COLUMN dwd_zrr_ymjzxx_new.scqy IS '生产企业';
COMMENT ON COLUMN dwd_zrr_ymjzxx_new.jzrq IS '接种日期';
COMMENT ON COLUMN dwd_zrr_ymjzxx_new.jzbw IS '接种部位';
COMMENT ON COLUMN dwd_zrr_ymjzxx_new.jzys IS '接种医生';
COMMENT ON COLUMN dwd_zrr_ymjzxx_new.jzjgbm IS '接种机构编码';
COMMENT ON COLUMN dwd_zrr_ymjzxx_new.fybz IS '费用标志';