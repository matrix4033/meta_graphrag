CREATE TABLE dwd_zrr_qygxxx_new (
    zrrwybs VARCHAR(200),
    sfzjlx CHAR(50),
    sfzjhm VARCHAR(200),
    bjhrxm VARCHAR(800),
    jhrsfzjlx VARCHAR(100),
    jhrsfzjhm VARCHAR(800),
    jhrxm VARCHAR(100),
    jhgx VARCHAR(100),
    fqsfzjlx VARCHAR(100),
    fqsfzjhm VARCHAR(800),
    fqxm VARCHAR(100),
    mqsfzjlx VARCHAR(100),
    mqsfzjhm VARCHAR(800),
    mqxm VARCHAR(100)
);

COMMENT ON TABLE dwd_zrr_qygxxx_new IS '亲缘关系信息';
COMMENT ON COLUMN dwd_zrr_qygxxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_qygxxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_qygxxx_new.sfzjhm IS '被监护人身份证件号码';
COMMENT ON COLUMN dwd_zrr_qygxxx_new.bjhrxm IS '被监护人姓名';
COMMENT ON COLUMN dwd_zrr_qygxxx_new.jhrsfzjlx IS '监护人身份证件类型';
COMMENT ON COLUMN dwd_zrr_qygxxx_new.jhrsfzjhm IS '监护人身份证件号码';
COMMENT ON COLUMN dwd_zrr_qygxxx_new.jhrxm IS '监护人姓名';
COMMENT ON COLUMN dwd_zrr_qygxxx_new.jhgx IS '监护关系';
COMMENT ON COLUMN dwd_zrr_qygxxx_new.fqsfzjlx IS '父亲身份证件类型';
COMMENT ON COLUMN dwd_zrr_qygxxx_new.fqsfzjhm IS '父亲身份证件号码';
COMMENT ON COLUMN dwd_zrr_qygxxx_new.fqxm IS '父亲姓名';
COMMENT ON COLUMN dwd_zrr_qygxxx_new.mqsfzjlx IS '母亲身份证件类型';
COMMENT ON COLUMN dwd_zrr_qygxxx_new.mqsfzjhm IS '母亲身份证件号码';
COMMENT ON COLUMN dwd_zrr_qygxxx_new.mqxm IS '母亲姓名';