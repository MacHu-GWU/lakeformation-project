代码设计文档
==============================================================================
Lakeformation 的 Data Access Model 是遵循: Principal, Resource, Permission 铁三角模型的. 一个 Access Policy 的本质就是, 谁 (Principal), 可以对 什么 (Resource) 做些什么 (Permission).

而对于 Lakeformation 所有的权限定义以及部署, 本质上就是管理这三者的关系. Lakeformation 服务本身不负责 创建, 管理, 删除 Principal 和 Resource. Principal 主要是 IAM, 由 IAM 服务管理. Resource 主要是 Data Catalog, 由 Glue Data Catalog 管理. 而 LakeFormation 主要负责的是定义 LF Tag, 以及 Tag 和 Principal / Resource 之间的绑定关系.

在我们的 Python 实现中, 会有很多类. 对于每个 LakeFormation 中的原生抽象概念, 我们都会定义一个类. 而对于一个最小的部署单位, 我们将其定义为一个 ``Playbook``. 一个 ``Playbook`` 的管理范围包括 ``LfTag``, ``LfTag / Principal / Permission binding``, ``LfTag / Resource binding``. 也就是说一个 ``Playbook`` 中会有很多属性, 通常是 ``LfTag`` 等对象的 collection 数据结构. 每次部署时候将这些被定义的数据结构用 CRUD API 进行 创建, 更新, 删除. 并把当前的 ``Playbook`` 序列化成 JSON 保存. 以后每次有新的部署, 都会和上一次的 Playbook 进行比较, 找到差异部分, 并对其进行更新即可.