CREATE TABLE dwd_zrr_cyzgxx_new (
    zrrwybs VARCHAR(800),
    sfzjlx VARCHAR(100),
    sfzjhm VARCHAR(800),
    zyzgzjbh VARCHAR(300),
    zyzgzjmc VARCHAR(100),
    zyzgzjlx VARCHAR(200),
    zyzgzjqfjgmc VARCHAR(100),
    zyzgzjqfjgdm VARCHAR(201),
    zyzgzjzt VARCHAR(202),
    zyzgzjyxqq DATE,
    zyzgzjyxqz DATE,
    zyzgzjqfrq DATE,
    zyzgzjccqfrq DATE,
    zyzgzjzxyy VARCHAR(100)
);

COMMENT ON TABLE dwd_zrr_cyzgxx_new IS '从业资格信息';
COMMENT ON COLUMN dwd_zrr_cyzgxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_cyzgxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_cyzgxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_cyzgxx_new.zyzgzjbh IS '证件编号';
COMMENT ON COLUMN dwd_zrr_cyzgxx_new.zyzgzjmc IS '证件名称';
COMMENT ON COLUMN dwd_zrr_cyzgxx_new.zyzgzjlx IS '证件类型';
COMMENT ON COLUMN dwd_zrr_cyzgxx_new.zyzgzjqfjgmc IS '证件签发机关名称';
COMMENT ON COLUMN dwd_zrr_cyzgxx_new.zyzgzjqfjgdm IS '从业资格证件签发机关代码';
COMMENT ON COLUMN dwd_zrr_cyzgxx_new.zyzgzjzt IS '证件状态';
COMMENT ON COLUMN dwd_zrr_cyzgxx_new.zyzgzjyxqq IS '证件有效期起';
COMMENT ON COLUMN dwd_zrr_cyzgxx_new.zyzgzjyxqz IS '证件有效期止';
COMMENT ON COLUMN dwd_zrr_cyzgxx_new.zyzgzjqfrq IS '证件签发日期';
COMMENT ON COLUMN dwd_zrr_cyzgxx_new.zyzgzjccqfrq IS '从业资格证件初次签发日期';
COMMENT ON COLUMN dwd_zrr_cyzgxx_new.zyzgzjzxyy IS '证件注销原因';