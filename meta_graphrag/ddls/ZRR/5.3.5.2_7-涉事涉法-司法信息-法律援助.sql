CREATE TABLE dwd_zrr_flyz_new (
    zrrwybs VARCHAR(1000),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(1000),
    ah VARCHAR(1000),
    yzfs VARCHAR(1000),
    slsj TIMESTAMP,
    sjajmc VARCHAR(1000),
    zdyy VARCHAR(1000),
    zdjg VARCHAR(1000),
    ajlb VARCHAR(1000),
    scrq DATE,
    ajcbr VARCHAR(1000),
    ajcbdw VARCHAR(1000)
);

COMMENT ON TABLE dwd_zrr_flyz_new IS '法律援助';
COMMENT ON COLUMN dwd_zrr_flyz_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_flyz_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_flyz_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_flyz_new.ah IS '案号';
COMMENT ON COLUMN dwd_zrr_flyz_new.yzfs IS '援助方式';
COMMENT ON COLUMN dwd_zrr_flyz_new.slsj IS '受理时间';
COMMENT ON COLUMN dwd_zrr_flyz_new.sjajmc IS '涉及案件名称';
COMMENT ON COLUMN dwd_zrr_flyz_new.zdyy IS '指定原因';
COMMENT ON COLUMN dwd_zrr_flyz_new.zdjg IS '指定机关';
COMMENT ON COLUMN dwd_zrr_flyz_new.ajlb IS '案件类别';
COMMENT ON COLUMN dwd_zrr_flyz_new.scrq IS '审查日期';
COMMENT ON COLUMN dwd_zrr_flyz_new.ajcbr IS '案件承办人';
COMMENT ON COLUMN dwd_zrr_flyz_new.ajcbdw IS '案件承办单位';