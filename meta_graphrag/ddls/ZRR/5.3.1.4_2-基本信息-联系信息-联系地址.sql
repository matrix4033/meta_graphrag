CREATE TABLE dwd_zrr_lxdz_new (
    zrrwybs VARCHAR(200),
    sfzjlx CHAR(50),
    sfzjhm VARCHAR(200),
    dzbm CHAR(200),
    dzmc VARCHAR(1000),
    ssqx CHAR(600),
    xzhjdmc VARCHAR(1000),
    xzchsq VARCHAR(1000)
);

COMMENT ON TABLE dwd_zrr_lxdz_new IS '联系地址';
COMMENT ON COLUMN dwd_zrr_lxdz_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_lxdz_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_lxdz_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_lxdz_new.dzbm IS '地址编码';
COMMENT ON COLUMN dwd_zrr_lxdz_new.dzmc IS '地址名称';
COMMENT ON COLUMN dwd_zrr_lxdz_new.ssqx IS '省市区县';
COMMENT ON COLUMN dwd_zrr_lxdz_new.xzhjdmc IS '乡镇或街道名称';
COMMENT ON COLUMN dwd_zrr_lxdz_new.xzchsq IS '行政村或社区';