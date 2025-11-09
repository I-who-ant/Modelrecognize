# Day32: Image Generation - 图像生成提示词模板库

> **应用场景**: 文生图、风格控制、细节优化、场景构图、角色设计等

---

## 📝 场景概述

### 核心挑战
- 准确描述视觉元素和细节
- 控制风格和氛围
- 避免AI误解或偏差
- 获得可重复的稳定结果

### 技术要求
- 使用精确的视觉描述语言
- 了解不同模型的特性
- 掌握权重和参数控制
- 理解提示词的优先级

---

## 🎯 快速模板库

### 模板1: 基础文生图

```
{主体描述}, {环境/背景}, {光线}, {风格}, {质量词}

主体: {详细描述主要对象}
环境: {场景和背景元素}
光线: {光照条件和氛围}
风格: {艺术风格或参考}
质量: {高质量、细节丰富等}

负面提示词(Negative): {要避免的元素}
```

**示例 - 风景照片**:
```
正面提示词:
A serene mountain lake at sunset, crystal clear water reflecting snow-capped peaks,
surrounded by pine forests, golden hour lighting, warm orange and pink sky,
misty atmosphere, professional landscape photography, ultra detailed, 8K resolution,
sharp focus, vivid colors

中文版:
宁静的山间湖泊,日落时分,清澈的湖水倒映着雪山,
周围环绕着松树林,黄金时段光线,温暖的橙粉色天空,
薄雾氛围,专业风景摄影,超高细节,8K分辨率,
锐利焦点,鲜艳色彩

负面提示词:
blurry, low quality, distorted, ugly, oversaturated, people, buildings,
modern objects, noise, artifacts

中文负面词:
模糊,低质量,扭曲,丑陋,过饱和,人物,建筑物,
现代物品,噪点,伪影

参数建议:
- 模型: Midjourney v6 或 SDXL
- 比例: 16:9 (风景)
- Steps: 30-50
- CFG Scale: 7-9
```

---

### 模板2: 角色设计

```
{角色基本信息}, {外貌特征}, {服装}, {姿态表情},
{背景}, {艺术风格}, {视角}, {光线}, {质量词}

角色: 年龄、性别、种族、职业
外貌: 发型、眼睛、面部特征、体型
服装: 详细的服饰描述
姿态: 动作和表情
背景: 简单或详细的背景
风格: 插画/写实/动漫等
```

**示例 - 奇幻角色**:
```
正面提示词:
A young elven archer, female, early 20s, long flowing silver hair with braids,
piercing emerald green eyes, delicate facial features, pointed ears,
wearing elegant leather armor with intricate leaf patterns,
forest green cloak, quiver of arrows on back,
standing in heroic pose, confident expression, bow in hand,
enchanted forest background with glowing mushrooms,
fantasy illustration style, anime-inspired, soft diffused lighting,
rim light highlighting hair, detailed character design, high quality, 4K

中文版:
年轻的精灵弓箭手,女性,20岁出头,银色长发带辫子,
锐利的翠绿色眼睛,精致的面部特征,尖耳朵,
穿着优雅的皮甲,带有精美的叶子图案,
森林绿色斗篷,背后挎着箭筒,
英雄姿态站立,自信的表情,手持弓箭,
魔法森林背景,发光的蘑菇,
奇幻插画风格,受动漫启发,柔和漫射光线,
轮廓光突出头发,精细的角色设计,高质量,4K

负面提示词:
ugly, deformed, extra limbs, bad anatomy, low quality, blurry,
modern clothing, realistic photo, oversexualized

参数建议:
- 风格: Anime/Fantasy Art
- 比例: 2:3 (竖版人物)
- 细节层次: High
```

---

### 模板3: 产品渲染

```
{产品名称和类型}, {材质}, {颜色}, {细节特征},
{摆放方式}, {背景}, {光线}, {渲染风格}, {质量词}

重点:
- 突出产品特点
- 材质真实感
- 专业摄影/渲染效果
```

**示例 - 智能手表**:
```
正面提示词:
Premium smartwatch with circular AMOLED display, sleek titanium case,
sapphire crystal glass, black leather strap with silver buckle,
showing fitness app interface on screen,
placed on minimalist white marble surface,
studio lighting setup, soft box from top left, rim light on right,
subtle reflections on polished surface,
product photography, commercial advertising style,
ultra realistic, 3D render quality, octane render,
8K resolution, perfect focus, clean composition

中文版:
高端智能手表,圆形AMOLED屏幕,光滑的钛金属表壳,
蓝宝石水晶玻璃,黑色皮革表带配银色表扣,
屏幕显示健身应用界面,
摆放在简约的白色大理石表面,
摄影棚灯光布置,左上方柔光箱,右侧轮廓光,
抛光表面的细微反射,
产品摄影,商业广告风格,
超写实,3D渲染质量,Octane渲染器,
8K分辨率,完美对焦,干净构图

负面提示词:
low quality, blurry, cheap looking, plastic, scratches,
fingerprints, cluttered background, poor lighting

参数建议:
- 风格: Photorealistic Product Render
- 比例: 1:1 或 4:5
- 重点: 材质和光线真实感
```

---

### 模板4: 场景概念设计

```
{场景类型}, {时代/风格}, {主要元素}, {氛围},
{光线和天气}, {视角}, {色调}, {细节描述}, {艺术风格}

适用: 游戏场景、电影概念图、建筑可视化
```

**示例 - 赛博朋克城市**:
```
正面提示词:
Cyberpunk megacity street at night, towering neon skyscrapers,
holographic advertisements floating in the air, flying cars,
rain-soaked streets reflecting colorful lights,
street vendors with glowing food carts, crowds of people in futuristic clothing,
steam rising from vents, power lines crisscrossing overhead,
viewed from street level looking up, wide angle perspective,
dominant colors: electric blue, hot pink, neon purple,
gritty urban atmosphere, blade runner aesthetic,
highly detailed environment concept art, digital painting,
cinematic lighting, volumetric fog, 4K, artstation quality

中文版:
赛博朋克超级城市夜景,高耸的霓虹摩天大楼,
全息广告漂浮在空中,飞行汽车,
雨水浸湿的街道反射着彩色灯光,
街边摊贩和发光的餐车,穿着未来服装的人群,
通风口冒出蒸汽,头顶纵横交错的电线,
从街道水平视角仰视,广角透视,
主色调:电蓝色、荧光粉、霓虹紫,
粗粝的都市氛围,银翼杀手美学,
高度细节的环境概念艺术,数字绘画,
电影级光照,体积雾效,4K,ArtStation质量

负面提示词:
daytime, clean, empty, low detail, cartoon, low quality

参数建议:
- 风格: Concept Art/Sci-Fi
- 比例: 16:9
- 氛围词权重: (cyberpunk:1.3), (neon lights:1.2)
```

---

### 模板5: 艺术风格模仿

```
{主题内容}, in the style of {艺术家/流派},
{该风格的特征描述}, {技法}, {色调}, {质量词}

常见风格:
- 印象派: Claude Monet, soft brushstrokes, light and color
- 立体派: Pablo Picasso, geometric shapes, multiple perspectives
- 浮世绘: Hokusai, flat colors, bold outlines, Japanese woodblock
- 数字艺术: Artgerm, Ross Tran, vibrant colors, anime influence
```

**示例 - 梵高风格**:
```
正面提示词:
A starry night over a small village, in the style of Vincent van Gogh,
swirling brushstrokes, thick impasto texture, bold and expressive,
vibrant blues and yellows, dramatic movement in the sky,
cypress trees in foreground, small houses with glowing windows,
post-impressionism, oil painting on canvas,
emotional and dynamic, masterpiece quality

中文版:
小村庄上的星空,梵高风格,
旋转的笔触,厚重的堆色肌理,大胆而富有表现力,
鲜艳的蓝色和黄色,天空中的戏剧性运动,
前景的柏树,窗户发光的小房子,
后印象派,布面油画,
情感化和动态的,大师级质量

负面提示词:
photorealistic, smooth, digital, modern, low quality

风格关键词:
- (Van Gogh style:1.4)
- (swirling brushstrokes:1.3)
- (impasto:1.2)
- (post-impressionism:1.2)
```

---

### 模板6: 权重控制和组合

```
使用权重语法精确控制元素:
- (keyword:1.2) - 增强20%
- (keyword:0.8) - 减弱20%
- [keyword1:keyword2:0.5] - 前50%步骤用keyword1,后50%用keyword2

组合技巧:
主要元素(高权重) + 次要元素(正常) + 避免元素(负权重)
```

**示例 - 精确控制的肖像**:
```
正面提示词(带权重):
(professional portrait:1.3), young woman, (beautiful face:1.2),
(detailed eyes:1.3), (soft smile:0.9),
long brown hair, (natural lighting:1.2), (bokeh background:1.1),
wearing casual sweater, (warm color palette:1.1),
(high quality:1.3), (sharp focus on face:1.2),
(soft focus on background:1.1), (shallow depth of field:1.2),
professional photography, 85mm lens, f/1.8

中文版(带权重):
(专业肖像:1.3),年轻女性,(美丽的面容:1.2),
(细节丰富的眼睛:1.3),(柔和的微笑:0.9),
棕色长发,(自然光线:1.2),(背景虚化:1.1),
穿着休闲毛衣,(温暖色调:1.1),
(高质量:1.3),(面部清晰对焦:1.2),
(背景柔焦:1.1),(浅景深:1.2),
专业摄影,85mm镜头,f/1.8

权重说明:
- 最高权重(1.3): 专业肖像、眼睛细节、高质量
- 高权重(1.2): 面容、光线、焦点、景深
- 正常权重(1.0): 默认元素
- 降低权重(0.9): 微笑(不要太明显)

负面提示词(带权重):
(low quality:1.4), (blurry:1.3), (distorted face:1.5),
(bad anatomy:1.3), ugly, deformed, (harsh lighting:1.2)
```

---

### 模板7: 分步细化(Prompt Evolution)

```
第一步: 基础构图
{简单描述主体和场景}

第二步: 添加细节
{补充材质、光线、颜色}

第三步: 风格定义
{艺术风格、质量要求}

第四步: 参数优化
{调整权重、负面词}
```

**示例 - 迭代优化过程**:
```
第一版(基础):
"A dragon flying over a castle"
结果: 基本元素有,但不够精彩

第二版(添加细节):
"A majestic red dragon with large wings flying over a medieval stone castle,
sunset sky, mountains in background"
结果: 更好,但风格不够突出

第三版(风格化):
"A majestic red dragon with large wings and sharp scales,
breathing fire, flying over a medieval stone castle with towers,
dramatic sunset sky with orange and purple clouds,
snow-capped mountains in background,
epic fantasy art, digital painting, cinematic lighting,
highly detailed, 4K"
结果: 接近目标,但需要微调

第四版(精细调优):
"(epic fantasy scene:1.3), a (majestic red dragon:1.2) with
(large powerful wings:1.2) and (detailed scales:1.1),
(breathing fire:1.2), flying over a (medieval stone castle:1.1)
with multiple towers,
(dramatic sunset sky:1.2) with vibrant orange and purple clouds,
snow-capped mountains in distant background,
(fantasy art:1.2), digital painting, (cinematic lighting:1.3),
(highly detailed:1.2), volumetric lighting, 4K resolution,
trending on artstation

Negative: low quality, blurry, cartoon, simple, flat colors,
(modern objects:1.3), people, text"
结果: ✅ 达到预期效果

关键改进:
1. 添加权重强调重点元素
2. 使用"trending on artstation"提升质量
3. 完善负面词排除不想要的元素
4. 添加"volumetric lighting"增强氛围
```

---

### 模板8: 特定模型优化

```
不同模型的提示词策略:

Midjourney:
- 简洁自然语言
- 使用 --v 6, --ar 16:9, --stylize 100 等参数
- 风格词如: cinematic, photorealistic, anime

Stable Diffusion:
- 详细关键词堆砌
- 使用权重 (keyword:1.2)
- 负面提示词很重要

DALL-E 3:
- 自然语言描述
- 详细的场景说明
- 较少需要技术参数
```

**示例 - 同一主题不同模型**:

```
主题: 未来派建筑

【Midjourney版本】
futuristic skyscraper, sleek white and glass design,
organic flowing curves, surrounded by green terraces,
sunset lighting, aerial view, architectural photography
--v 6 --ar 16:9 --stylize 250

【Stable Diffusion版本】
(futuristic architecture:1.3), towering skyscraper,
(sleek design:1.2), white facade and (reflective glass:1.2),
(organic flowing curves:1.2), (vertical gardens:1.1),
green terraces with plants, (golden hour lighting:1.2),
aerial view from drone, (architectural photography:1.2),
(ultra detailed:1.3), (photorealistic:1.2), 8K,
sharp focus, professional

Negative: low quality, blurry, distorted, ugly,
cluttered, old buildings, dark, night

【DALL-E 3版本】
A stunning futuristic skyscraper photographed from an aerial view.
The building features a sleek, modern design with white facade and
reflective glass panels that curve organically upward.
Lush green terraces with plants wrap around multiple levels,
creating vertical gardens throughout the structure.
The scene is captured during golden hour, with warm sunset light
illuminating the building's flowing curves.
The photograph is professional architectural photography,
ultra detailed and photorealistic in 8K resolution.

对比:
- MJ: 简洁,依赖参数控制
- SD: 关键词密集,权重控制
- DALL-E 3: 完整句子,自然描述
```

---

## 💡 最佳实践

### 1. 提示词结构优先级

```
优先级从高到低:
1. 主体(最重要) - 核心对象
2. 质量词 - masterpiece, high quality, detailed
3. 风格 - 艺术风格或参考
4. 光线 - lighting, time of day
5. 视角 - camera angle, perspective
6. 细节 - 材质、颜色、纹理
7. 背景 - 次要元素
```

### 2. 常用质量提升词

```
通用:
- high quality, masterpiece, best quality
- ultra detailed, extremely detailed
- 4K, 8K, high resolution
- sharp focus, crisp

摄影类:
- professional photography
- DSLR, 85mm lens, f/1.4
- bokeh, depth of field
- studio lighting, golden hour

艺术类:
- trending on artstation
- award winning
- by famous artist
- museum quality
```

### 3. 常见负面词

```
质量类:
- low quality, worst quality
- blurry, out of focus
- pixelated, jpeg artifacts
- low resolution

解剖类(人物):
- bad anatomy, extra limbs
- deformed, mutated
- bad proportions
- missing fingers

风格类:
- ugly, amateur
- simple, plain
- cartoon (如果要写实)
- watermark, signature, text
```

---

## 🔧 技术融合

### 结合前置技术

```
Day7: Few-Shot
└─ 提供参考图片示例引导风格

Day25: Diversity
└─ 生成多样化的图像变体

组合使用:
1. 文字描述(Prompt)
2. 参考图(Image-to-Image)
3. 控制网络(ControlNet)
4. 局部重绘(Inpainting)
```

---

## ⚠️ 常见陷阱

### 陷阱1: 描述过于简单

```
❌ 错误:
"a beautiful woman"

✅ 正确:
"professional portrait of an elegant woman in her 30s,
long black hair, gentle smile, wearing pearl earrings,
soft natural lighting, shallow depth of field,
photography by Annie Leibovitz style,
high quality, 4K"
```

### 陷阱2: 矛盾的描述

```
❌ 错误:
"photorealistic anime character"
(照片写实 vs 动漫风格冲突)

✅ 正确:
明确选择一种风格:
"photorealistic portrait" 或
"anime style character illustration"
```

### 陷阱3: 忽略负面词

```
❌ 错误:
只写正面描述,不写负面词
结果: 可能出现低质量、变形等问题

✅ 正确:
总是添加基础负面词:
"Negative: low quality, blurry, distorted, bad anatomy"
```

---

## 📚 参考资源

**提示词数据库**:
- Lexica.art - Stable Diffusion提示词
- PromptHero - 多模型提示词
- Midjourney Community Feed

**学习资源**:
- Prompt Engineering for Image Generation
- Stable Diffusion Prompt Guide
- Midjourney Documentation

---

**下一步**: Day33 - Mathematics (数学问题提示词)
