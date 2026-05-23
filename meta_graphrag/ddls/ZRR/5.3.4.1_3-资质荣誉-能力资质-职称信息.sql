CREATE TABLE dwd_zrr_zcxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx VARCHAR(50),
    sfzjhm VARCHAR(800),
    xm VARCHAR(400),
    zcmc VARCHAR(2000),
    xcszyjsgz VARCHAR(2000),
    dwmc VARCHAR(2000),
    xxzzw VARCHAR(2000),
    pdsj DATE
);

COMMENT ON TABLE dwd_zrr_zcxx_new IS '职称信息';
COMMENT ON COLUMN dwd_zrr_zcxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_zcxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_zcxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_zcxx_new.xm IS '姓名';
COMMENT ON COLUMN dwd_zrr_zcxx_new.zcmc IS '职称名称';
COMMENT ON COLUMN dwd_zrr_zcxx_new.xcszyjsgz IS '现从事专业技术工作';
COMMENT ON COLUMN dwd_zrr_zcxx_new.dwmc IS '单位名称';
COMMENT ON COLUMN dwd_zrr_zcxx_new.xxzzw IS '现行政职务';
COMMENT ON COLUMN dwd_zrr_zcxx_new.pdsj IS '评定时间';