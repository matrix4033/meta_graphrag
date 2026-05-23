CREATE TABLE dwd_zrr_zyzgxx_new (
    zrrwybs VARCHAR(1600),
    sfzjlx CHAR(400),
    sfzjhm VARCHAR(1600),
    zjbh VARCHAR(2000),
    zjmc VARCHAR(800),
    zjlx VARCHAR(3200),
    zjqfjgmc VARCHAR(2000),
    zjqfjgdm VARCHAR(1280),
    zjzt CHAR(1600),
    zjyxqq DATE,
    zjyxqz DATE,
    zjqfrq DATE,
    xzzfssdq VARCHAR(2000),
    zjccqfrq VARCHAR(1600),
    zjzxrq DATE,
    zjzxyy VARCHAR(4000),
    xzqh VARCHAR(3200),
    jszc VARCHAR(4000),
    xb VARCHAR(2000),
    xm VARCHAR(2000),
    mz VARCHAR(1500),
    gzks VARCHAR(3200),
    gj VARCHAR(3200),
    zyzyjg VARCHAR(3200),
    zyfw VARCHAR(3200),
    zjszdq VARCHAR(1600),
    zjyxq DATE,
    zyjb VARCHAR(400),
    rzzg VARCHAR(800),
    zzmm VARCHAR(3000),
    sjhm_encode VARCHAR(2400),
    zydwlxdh_encode VARCHAR(3000)
);

COMMENT ON TABLE dwd_zrr_zyzgxx_new IS '执业资格信息';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zjbh IS '证件编号';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zjmc IS '证件名称';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zjlx IS '证件类型';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zjqfjgmc IS '证件签发机关名称';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zjqfjgdm IS '证件签发机关代码';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zjzt IS '证件状态';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zjyxqq IS '证件有效期起';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zjyxqz IS '证件有效期止';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zjqfrq IS '证件签发日期';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.xzzfssdq IS '行政执法所属地区';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zjccqfrq IS '证件初次签发日期';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zjzxrq IS '证件注销日期';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zjzxyy IS '证件注销原因';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.xzqh IS '行政区划';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.jszc IS '技术职称';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.xb IS '性别';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.xm IS '姓名';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.mz IS '民族';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.gzks IS '工作科室';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.gj IS '国籍';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zyzyjg IS '主要执业机构';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zyfw IS '执业范围';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zjszdq IS '证件所在地区';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zjyxq IS '证件有效期';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zyjb IS '执业级别';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.rzzg IS '任职资格';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zzmm IS '政治面貌';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.sjhm_encode IS '手机号码';
COMMENT ON COLUMN dwd_zrr_zyzgxx_new.zydwlxdh_encode IS '执业单位联系电话';