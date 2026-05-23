CREATE TABLE dwd_zrr_bdcqzxx_new (
    zrrwybs VARCHAR(800),
    cqzbh VARCHAR(5000),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    bdcqdjsj DATE,
    bdcdyh CHAR(224),
    bdcdjjg VARCHAR(400),
    bdcqgyfs VARCHAR(1600),
    bdcgyqk VARCHAR(32000),
    bdcqlxz VARCHAR(800),
    bdcqllx VARCHAR(800),
    fwyt VARCHAR(1000),
    scjzmj VARCHAR(400),
    qszt VARCHAR(10),
    fwzl VARCHAR(3000)
);

COMMENT ON TABLE dwd_zrr_bdcqzxx_new IS '不动产权利信息表';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.cqzbh IS '产权证编号';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.bdcqdjsj IS '不动产登记时间';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.bdcdyh IS '不动产单元号';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.bdcdjjg IS '不动产登记机构';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.bdcqgyfs IS '不动产权共有方式';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.bdcgyqk IS '不动产共有情况';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.bdcqlxz IS '不动产权利性质';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.bdcqllx IS '不动产权利类型';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.fwyt IS '房屋用途';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.scjzmj IS '实测建筑面积';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.qszt IS '权属状态';
COMMENT ON COLUMN dwd_zrr_bdcqzxx_new.fwzl IS '房屋坐落';