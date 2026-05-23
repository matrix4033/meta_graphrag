CREATE TABLE dwd_swk_swrykzxxb_new (
    id BIGINT,
    ryid VARCHAR(64),
    swkbh VARCHAR(32),
    hhzmbh VARCHAR(20),
    swyy_mz VARCHAR(8),
    swrq_mz VARCHAR(8),
    swrq_wj VARCHAR(8),
    swrq_yb VARCHAR(8),
    ywrq_rs VARCHAR(8),
    hhrq VARCHAR(8),
    jarg VARCHAR(8),
    ah VARCHAR(50),
    dwmc_mz VARCHAR(200),
    data_create_time TIMESTAMP(14),
    data_update_time TIMESTAMP(14)
);

COMMENT ON TABLE dwd_swk_swrykzxxb_new IS '死亡人员扩展信息';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.id IS '自增主键';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.ryid IS '自然人口';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.swkbh IS '死亡卡编号';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.hhzmbh IS '火化证明编号';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.swyy_mz IS '死亡原因(民政)';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.swrq_mz IS '死亡日期(民政)';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.swrq_wj IS '死亡日期(卫健)';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.swrq_yb IS '死亡日期(医保)';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.ywrq_rs IS '业务日期（人社）';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.hhrq IS '火化日期';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.jarg IS '结案日期';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.ah IS '案号';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.dwmc_mz IS '单位名称(民政)';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.data_create_time IS '数据入库时间';
COMMENT ON COLUMN dwd_swk_swrykzxxb_new.data_update_time IS '数据变动时间';