CREATE TABLE dwd_zrr_ryxx_new (
    zrrwybs VARCHAR(1600),
    sfzjlx CHAR(400),
    sfzjhm VARCHAR(1600),
    rzyrymc VARCHAR(1600),
    yxq CHAR(32),
    rymc VARCHAR(400),
    shzt VARCHAR(800),
    ryjb VARCHAR(240),
    jb VARCHAR(1000),
    zslx TEXT,
    ryrdrq DATE,
    ryjldx VARCHAR(800),
    zsbh TEXT,
    ryzsyxqz VARCHAR(240),
    ryzsyxqzh VARCHAR(240),
    rybfjgmc VARCHAR(400)
);

COMMENT ON TABLE dwd_zrr_ryxx_new IS '荣誉信息';
COMMENT ON COLUMN dwd_zrr_ryxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_ryxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_ryxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_ryxx_new.rzyrymc IS '认证与荣誉名称';
COMMENT ON COLUMN dwd_zrr_ryxx_new.yxq IS '有效期';
COMMENT ON COLUMN dwd_zrr_ryxx_new.rymc IS '荣誉名称';
COMMENT ON COLUMN dwd_zrr_ryxx_new.shzt IS '审核状态';
COMMENT ON COLUMN dwd_zrr_ryxx_new.ryjb IS '荣誉级别';
COMMENT ON COLUMN dwd_zrr_ryxx_new.jb IS '级别';
COMMENT ON COLUMN dwd_zrr_ryxx_new.zslx IS '证书类型';
COMMENT ON COLUMN dwd_zrr_ryxx_new.ryrdrq IS '荣誉认定日期';
COMMENT ON COLUMN dwd_zrr_ryxx_new.ryjldx IS '荣誉奖励对象';
COMMENT ON COLUMN dwd_zrr_ryxx_new.zsbh IS '证书编号';
COMMENT ON COLUMN dwd_zrr_ryxx_new.ryzsyxqz IS '荣誉证书有效期自';
COMMENT ON COLUMN dwd_zrr_ryxx_new.ryzsyxqzh IS '荣誉证书有效期至';
COMMENT ON COLUMN dwd_zrr_ryxx_new.rybfjgmc IS '荣誉颁发机构名称';