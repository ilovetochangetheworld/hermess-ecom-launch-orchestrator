# Orchestration Prompts

Use these prompts to run the workflow consistently.

## Full Workflow

```text
你是 Hermess 电商全链路总控 Agent。请把一个商品从选品分析推进到可发布、可客服、可复盘的完整闭环。

演示模式：{live|mock|manual}
商品：{商品名称或现场商品描述}
目标平台：小红书
目标用户：{可选}
可用数据：
- Amazon竞品数据：{有|无|已粘贴}
- 1688供应数据：{有|无|已粘贴}
- 商品图片：{有|无}
- XHS Cookie：{已刷新|未刷新|不用真实发布}
- 评论数据：{有|无|使用样例}

请按以下阶段推进：
1. 选品竞品分析
2. 小红书种草文案
3. 产品图生成或图片 prompt
4. 发布或模拟发布
5. 智能客服 FAQ 和实时问答
6. 评论分析与下一轮选品回流

每个阶段必须输出：
- 当前阶段状态
- 已完成产物
- 缺失输入
- 是否触发 fallback
- 下一步动作

最终请合并为 workflow envelope，并给出适合现场讲解的 5 句话总结。
```

## Stage Recovery

```text
当前 Hermess 电商演示卡在以下阶段：

阶段：{research|copywriting|imaging|publishing|customer_service|review_analysis}
阻塞原因：{具体原因}
当前已有产物：{粘贴已有JSON或摘要}
剩余演示时间：{分钟}

请判断应该采用 live、mock 还是 manual 路径继续，并输出：
1. 推荐路径
2. 对观众的解释话术
3. 可继续展示的产物
4. 需要跳过或模拟的动作
5. 下一步操作
```

## Final Workshop Takeaway

```text
请把以下 workflow envelope 整理成观众可带走的提效工坊素材包。

{workflow_envelope_json}

输出：
1. 一句话价值总结
2. 六步流程图文案
3. 可复用 prompt 清单
4. 本次商品生成的素材列表
5. 下一次迁移到其他业务场景的方法
```
