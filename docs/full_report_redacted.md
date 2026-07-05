# Full Redacted Project Report

This public GitHub version keeps the complete technical report text while removing private identifiers such as student IDs and email addresses.

Original binary report files are intentionally not committed to the public repository because they may contain private front-matter metadata.

---

[FILE final_project/ACADEMIC_REVIEW.md]
# مراجعة أكاديمية شاملة - Campus Transit & Navigation System

## 1. نطاق المراجعة

تمت مراجعة ملف تعليمات المشروع كاملًا، قالب البرنامج، ملف الفحص المرفق، ملفي
CSV، ومحاضرات ومختبرات Graph, Directed Graph, Heap, Dijkstra, MST,
Kruskal, Prim-Jarnik وUnion-Find.

الملف المطلوب للتسليم هو `campus_nav.py` فقط. الملفات الأخرى الموجودة في
المجلد مخصّصة للتشغيل المحلي والتوثيق والتحقق وليست جزءًا من ملف التسليم.

## 2. مطابقة متطلبات المشروع

| مطلب المشروع | موضع التنفيذ | طريقة التحقق |
|---|---|---|
| ملف Python واحد باسم `campus_nav.py` | الملف النهائي نفسه | فحص الاسم والاستيراد من مجلد نظيف |
| الصنف `CampusNav` | `campus_nav.py` | استيراد الصنف وإنشاء كائنات متعددة |
| قراءة ملف CSV | `read_from_file` | الخريطتان الرسميتان وحالات CSV غير صالحة |
| فحص وجود مبنى | `inMap` | مبانٍ موجودة وغير موجودة |
| ملاحة تجمع المشي والشاتل | `Navigate` | حالات رسمية وعشوائية وbrute force |
| احتساب وقت انتظار الشاتل | دالة relaxation داخل `Navigate` | انطلاق فوري، بعد فوات شاتل، وعلى موعد الانطلاق |
| إعادة وقت الوصول والمسار | `Navigate` و`_build_path` | فحص الوقت وإعادة تشغيل كل حافة في المسار |
| Heap مكتوب يدويًا | `MinHeap` | invariant بعد كل إدخال وإزالة |
| رأس الـHeap في index 1 | `heapList = [None]` | فحص دائم أن `heapList[0] is None` |
| عدم استخدام `heapq` أو مكتبات رسوم بيانية | imports في ملف التسليم | تحليل AST وفحص imports |
| Fiber على طرق المشي فقط | `FiberOptic_deployment` | تجاهل جميع حواف shuttle وكلفة MST الرسمية |
| Minimum Spanning Tree | Kruskal مع Union-Find | مقارنة مع Kruskal مستقل وbrute force |
| Console UI بثلاثة خيارات | `main_menu` | تشغيل آلي وتشغيل فعلي من سطر الأوامر |

## 3. النموذج الرياضي

الخريطة شبكة موجّهة متعددة الحواف:

- `V`: المباني والمواقع.
- `E_walk`: طرق المشي الموجّهة كما تظهر في CSV.
- `E_shuttle`: خطوط الشاتل الموجّهة.
- يمكن وجود حافة مشي وحافة شاتل بين نفس الأصل والوجهة.

الخريطة الكبيرة تكرر طرق المشي بالاتجاه العكسي، ولذلك يصبح المشي ثنائي
الاتجاه عندما يحتوي CSV على السطرين. خطوط الشاتل غير مكررة وتبقى باتجاه واحد.

بالنسبة لتمديد الألياف، اتجاه طريق المشي لا يهم؛ لذلك يعامل Kruskal حافة المشي
كوصلة غير موجّهة. تكرار الطريق المعاكس لا يؤثر لأن Union-Find يرفض الحافة التي
تصنع دورة.

## 4. خوارزمية الملاحة الزمنية

إذا وصلنا إلى مبنى في الدقيقة `t`:

- المشي بحافة وزنها `w`: وقت الوصول الجديد `t + w`.
- الشاتل ذو interval يساوي `I`: موعد الانطلاق التالي هو
 `ceil(t / I) * I`، ووقت الوصول هو موعد الانطلاق زائد `w`.

تخزن الخوارزمية `arrival[v]`، أي أفضل وقت وصول معروف إلى كل مبنى، وتستخدم
MinHeap لاستخراج أصغر وقت. عند تحسين الوصول إلى مبنى، تحفظ `previous[v]`
لإعادة بناء المسار النهائي.

### برهان الصحة

دالة الوصول في طريق المشي متزايدة. ودالة وصول الشاتل
`ceil(t/I)*I + w` غير متناقصة: الوصول إلى المحطة أبكر لا يمنع الراكب من
انتظار نفس الشاتل الذي يستطيع راكب متأخر أخذه. هذه هي خاصية FIFO المطلوبة في
Time-Dependent Dijkstra.

لذلك، عندما يزيل الـHeap مبنى بأصغر وقت غير قديم، لا يمكن لأي مسار يبدأ من
مبنى غير محسوم أن يصل إليه أبكر. بالاستقراء، كل مبنى تتم إزالته لأول مرة يحمل
وقت الوصول الأمثل. وعند إزالة الوجهة، تكون سلسلة `previous` مسارًا يحقق ذلك
الوقت.

### التعقيد

- القراءة: `O(V + E)` وقت ومساحة.
- `inMap`: وقت متوقع `O(1)`.
- الملاحة: `O((V + E) log E)` باستخدام lazy heap entries، ومساحة
 `O(V + E)` في أسوأ حالة.

## 5. الـMinHeap

المصفوفة تبدأ بـ`[None]`، والجذر في index 1. أبناء العنصر `i` هما `2*i`
و`2*i+1`، والأب هو `i//2`.

- `insert`: إضافة في النهاية ثم upheap، بتعقيد `O(log n)`.
- `remove_min`: استبدال الجذر بآخر عنصر ثم downheap، بتعقيد `O(log n)`.
- العناصر ذات الأولوية المتساوية تزال حسب ترتيب إدخالها، مما يجعل اختيار
 المسارات والحواف حتميًا.

## 6. Kruskal وUnion-Find

تدخل حواف المشي فقط إلى MinHeap، فتخرج بترتيب الوزن. تقبل الحافة إذا كان
طرفاها في مجموعتين مختلفتين، ثم تدمج المجموعتان. تتوقف الخوارزمية عند جمع
`|V|-1` حافة.

بحسب خاصية القطع، أصغر حافة تصل بين مكوّنين مختلفين حافة آمنة لبعض MST.
تكرار هذه الخطوة ينتج spanning tree بأقل وزن. Union-Find يستخدم union-by-size
وpath compression لمنع الدورات وتسريع `find` و`union`.

التعقيد هو `O(E_walk log E_walk)` بسبب الـHeap، مع تكلفة شبه ثابتة amortized
لعمليات Union-Find. إذا كانت شبكة المشي غير متصلة، تعيد الدالة قائمة فارغة
لأنه لا توجد spanning tree تغطي جميع المباني.

## 7. التحقق من CSV والحالات الحدية

القارئ يتحقق من:

- وجود الأعمدة الخمسة المطلوبة.
- عدم فراغ `orig`, `dest`, `weight`.
- أن النوع `walk` أو `shuttle`.
- أن الوزن عددي وغير سالب.
- أن interval الشاتل موجود، عددي وموجب.
- تجاهل الأسطر الفارغة ودعم UTF-8 BOM.

تتم القراءة داخل بنى مؤقتة، ولا تستبدل الخريطة القديمة إلا بعد نجاح قراءة
الملف كاملًا. لذلك لا يفسد CSV غير صالح خريطة سبق تحميلها.

الحالات التي تم اختبارها تشمل: نقطة بداية تساوي الوجهة، مبنى غير موجود، وجهة
غير قابلة للوصول، graph غير متصل، حواف متوازية، أوزان متساوية، وقت غير صالح،
وشبكة تحتوي اتجاهات مختلفة.

## 8. نتائج التحقق

### الحالات الرسمية

- `MainGate -> Lab` عند الدقيقة 0: وصول 6، المسار
 `MainGate -> Library -> Lab`.
- `MainGate -> Library` عند الدقيقة 3: الشاتل التالي عند الدقيقة 10 والوصول
 عند الدقيقة 12.
- MST لخريطة الاختبار: 3 حواف، الكلفة 15.
- MST للخريطة الكبيرة: 11 حافة، الكلفة 59.

### الاختبارات المستقلة

- 2,000 إدخال عشوائي للـHeap مع فحص invariant بعد كل عملية.
- 1,728 استعلام ملاحة على 12 شبكة عشوائية، مقارنة مع oracle مستقل.
- 750 استعلامًا على 10 شبكات صغيرة، مقارنة مع تعداد شامل للمسارات البسيطة.
- 10 مسائل MST صغيرة، مقارنة مع تعداد شامل لجميع مجموعات الحواف الممكنة.
- إعادة تشغيل كل مسار ناتج حافةً حافة للتأكد أن وقت المسار يساوي الوقت المعاد.
- فحوص ملفات CSV غير صالحة وفحص transactional reload.
- فحص Console للخيارات الملاحة، الألياف والخروج.

### اختبار الحجم

على شبكة صناعية تحتوي 1,000 مبنى و5,998 سطر CSV:

- القراءة: نحو 0.080 ثانية.
- 20 استعلام ملاحة: نحو 0.087 ثانية إجمالًا.
- MST: نحو 0.024 ثانية، مع 999 حافة.
- أعلى ذاكرة متتبعة: نحو 2 MiB.

هذه أرقام قياس محلية وليست حدودًا مضمونة، لكنها تؤكد أن التنفيذ يتصرف وفق
التعقيد المتوقع على حجم أكبر كثيرًا من الملفات المرفقة.

## 9. ملاحظات حول ملف الفحص الأصلي

النسخة ذات الاسم الطويل من `code_tester` تحتوي أخطاء داخلية:

- تعليقها يحسب وصول 08:03 عند الدقيقة 12، ثم تتوقع 14.
- تستخدم `edge[3]` رغم أن واجهة القالب تعرّف حافة MST كثلاثية.
- تستخدم المتغير غير المعرّف `total_fiber_cost` بدل `total_cost`.

تم الحفاظ على الملف الأصلي دون تعديل، وإنشاء `code_tester.py` مصحح. النتيجة
12 متوافقة مع الحساب الرياضي ومع PDF الرسمي.

## 10. التشغيل والتسليم

للتشغيل المحلي:

```powershell
python campus_nav.py
python code_tester.py
python test_campus_nav.py
```

قبل التسليم يجب رفع `campus_nav.py` فقط، وعدم رفع ملفات الاختبار أو التوثيق.
يُنصح بقراءة الصنف `MinHeap`، relaxation في `Navigate`، وUnion-Find جيدًا حتى
يمكن شرح الحل والخطوات والتعقيد بوضوح.

[FILE final_project/campus_map.csv]
orig,dest,type,weight,interval
MainGate,Administration,walk,4,
MainGate,Engineering_Block,walk,12,
Administration,Engineering_Block,walk,6,
Administration,Arts_Center,walk,8,
Engineering_Block,Computer_Labs,walk,3,
Engineering_Block,Science_Tower,walk,10,
Computer_Labs,Library,walk,5,
Arts_Center,Library,walk,9,
Arts_Center,Student_Union,walk,4,
Student_Union,Sports_Center,walk,7,
Library,Medical_Clinic,walk,6,
Science_Tower,Medical_Clinic,walk,5,
Science_Tower,Dormitories_North,walk,14,
Medical_Clinic,Dormitories_North,walk,8,
Medical_Clinic,Dormitories_South,walk,11,
Sports_Center,Dormitories_South,walk,5,
Dormitories_North,Dormitories_South,walk,6,
Administration,MainGate,walk,4,
Engineering_Block,MainGate,walk,12,
Engineering_Block,Administration,walk,6,
Arts_Center,Administration,walk,8,
Computer_Labs,Engineering_Block,walk,3,
Science_Tower,Engineering_Block,walk,10,
Library,Computer_Labs,walk,5,
Library,Arts_Center,walk,9,
Student_Union,Arts_Center,walk,4,
Sports_Center,Student_Union,walk,7,
Medical_Clinic,Library,walk,6,
Medical_Clinic,Science_Tower,walk,5,
Dormitories_North,Science_Tower,walk,14,
Dormitories_North,Medical_Clinic,walk,8,
Dormitories_South,Medical_Clinic,walk,11,
Dormitories_South,Sports_Center,walk,5,
Dormitories_South,Dormitories_North,walk,6,
MainGate,Library,shuttle,4,15
MainGate,Science_Tower,shuttle,6,20
Student_Union,Dormitories_South,shuttle,2,10
Science_Tower,Dormitories_North,shuttle,3,12
Dormitories_North,MainGate,shuttle,8,30

[FILE final_project/campus_map_cafb22de3710fb65bbb51e158f4f7514.csv]
orig,dest,type,weight,interval

MainGate,Administration,walk,4,

MainGate,Engineering_Block,walk,12,

Administration,Engineering_Block,walk,6,

Administration,Arts_Center,walk,8,

Engineering_Block,Computer_Labs,walk,3,

Engineering_Block,Science_Tower,walk,10,

Computer_Labs,Library,walk,5,

Arts_Center,Library,walk,9,

Arts_Center,Student_Union,walk,4,

Student_Union,Sports_Center,walk,7,

Library,Medical_Clinic,walk,6,

Science_Tower,Medical_Clinic,walk,5,

Science_Tower,Dormitories_North,walk,14,

Medical_Clinic,Dormitories_North,walk,8,

Medical_Clinic,Dormitories_South,walk,11,

Sports_Center,Dormitories_South,walk,5,

Dormitories_North,Dormitories_South,walk,6,

Administration,MainGate,walk,4,

Engineering_Block,MainGate,walk,12,

Engineering_Block,Administration,walk,6,

Arts_Center,Administration,walk,8,

Computer_Labs,Engineering_Block,walk,3,

Science_Tower,Engineering_Block,walk,10,

Library,Computer_Labs,walk,5,

Library,Arts_Center,walk,9,

Student_Union,Arts_Center,walk,4,

Sports_Center,Student_Union,walk,7,

Medical_Clinic,Library,walk,6,

Medical_Clinic,Science_Tower,walk,5,

Dormitories_North,Science_Tower,walk,14,

Dormitories_North,Medical_Clinic,walk,8,

Dormitories_South,Medical_Clinic,walk,11,

Dormitories_South,Sports_Center,walk,5,

Dormitories_South,Dormitories_North,walk,6,

MainGate,Library,shuttle,4,15

MainGate,Science_Tower,shuttle,6,20

Student_Union,Dormitories_South,shuttle,2,10

Science_Tower,Dormitories_North,shuttle,3,12

Dormitories_North,MainGate,shuttle,8,30


[FILE final_project/campus_map_testcase1.csv]
orig,dest,type,weight,interval
MainGate,BuildingA,walk,5,
BuildingA,Library,walk,6,
MainGate,Library,walk,15,
Library,Lab,walk,4,
MainGate,Library,shuttle,2,10

[FILE final_project/campus_map_testcase1_b7ae70de2d8e2b84e9852f193a230f2c.csv]
orig,dest,type,weight,interval

MainGate,BuildingA,walk,5,

BuildingA,Library,walk,6,

MainGate,Library,walk,15,

Library,Lab,walk,4,

MainGate,Library,shuttle,2,10


[FILE final_project/campus_nav.py]
import csv
import math
import os

class MinHeap:
 """A stable minimum heap whose root is stored at index 1."""

 def __init__(self):
 self.heapList = [None]
 self.currentSize = 0
 self._next_order = 0

 def is_empty(self):
 return self.currentSize == 0

 def __len__(self):
 return self.currentSize

 def _less(self, first, second):
 return self.heapList[first][:2] < self.heapList[second][:2]

 def _upheap(self, index):
 while index > 1:
 parent = index // 2
 if not self._less(index, parent):
 break
 self.heapList[index], self.heapList[parent] = (
 self.heapList[parent],
 self.heapList[index],
 )
 index = parent

 def _downheap(self, index):
 while 2 * index <= self.currentSize:
 child = 2 * index
 if child + 1 <= self.currentSize and self._less(child + 1, child):
 child += 1
 if not self._less(child, index):
 break
 self.heapList[index], self.heapList[child] = (
 self.heapList[child],
 self.heapList[index],
 )
 index = child

 def insert(self, key, value):
 entry = (key, self._next_order, value)
 self._next_order += 1
 self.heapList.append(entry)
 self.currentSize += 1
 self._upheap(self.currentSize)

 def remove_min(self):
 if self.is_empty():
 raise IndexError("remove_min from an empty heap")

 minimum = self.heapList[1]
 last = self.heapList.pop()
 self.currentSize -= 1

 if self.currentSize:
 self.heapList[1] = last
 self._downheap(1)

 return minimum[0], minimum[2]

class UnionFind:
 """Disjoint sets with path compression and union by size."""

 def __init__(self, values):
 self.parent = {value: value for value in values}
 self.size = {value: 1 for value in values}

 def find(self, value):
 root = value
 while self.parent[root] != root:
 root = self.parent[root]

 while self.parent[value] != value:
 parent = self.parent[value]
 self.parent[value] = root
 value = parent

 return root

 def union(self, first, second):
 first_root = self.find(first)
 second_root = self.find(second)

 if first_root == second_root:
 return False

 if self.size[first_root] < self.size[second_root]:
 first_root, second_root = second_root, first_root

 self.parent[second_root] = first_root
 self.size[first_root] += self.size[second_root]
 return True

class CampusNav:
 REQUIRED_COLUMNS = ("orig", "dest", "type", "weight", "interval")

 def __init__(self):
 self._locations = {}
 self._adjacency = {}
 self._walk_edges = []

 @staticmethod
 def _number(text, field_name, line_number, positive=False):
 try:
 value = float(text)
 except (TypeError, ValueError) as error:
 raise ValueError(
 f"line {line_number}: {field_name} must be numeric"
 ) from error

 if not math.isfinite(value):
 raise ValueError(f"line {line_number}: {field_name} must be finite")
 if positive and value <= 0:
 raise ValueError(f"line {line_number}: {field_name} must be positive")
 if not positive and value < 0:
 raise ValueError(
 f"line {line_number}: {field_name} cannot be negative"
 )

 return int(value) if value.is_integer() else value

 def read_from_file(self, filename):
 """Read the campus CSV and replace the currently loaded map."""

 locations = {}
 adjacency = {}
 walk_edges = []

 with open(filename, "r", encoding="utf-8-sig", newline="") as source:
 reader = csv.DictReader(source)
 if reader.fieldnames is None:
 raise ValueError("CSV file is missing its header")

 reader.fieldnames = [
 name.strip() if name is not None else ""
 for name in reader.fieldnames
 ]
 missing = [
 name for name in self.REQUIRED_COLUMNS
 if name not in reader.fieldnames
 ]
 if missing:
 raise ValueError(
 "CSV header is missing: " + ", ".join(missing)
 )

 for line_number, row in enumerate(reader, start=2):
 values = [row.get(name) for name in self.REQUIRED_COLUMNS]
 if all(value is None or str(value).strip() == "" for value in values):
 continue

 origin = (row.get("orig") or "").strip()
 destination = (row.get("dest") or "").strip()
 edge_type = (row.get("type") or "").strip().lower()
 weight_text = (row.get("weight") or "").strip()
 interval_text = (row.get("interval") or "").strip()

 if not origin or not destination:
 raise ValueError(
 f"line {line_number}: orig and dest cannot be empty"
 )
 if edge_type not in ("walk", "shuttle"):
 raise ValueError(
 f"line {line_number}: type must be walk or shuttle"
 )
 if not weight_text:
 raise ValueError(f"line {line_number}: weight cannot be empty")

 weight = self._number(weight_text, "weight", line_number)
 interval = None
 if edge_type == "shuttle":
 if not interval_text:
 raise ValueError(
 f"line {line_number}: shuttle interval cannot be empty"
 )
 interval = self._number(
 interval_text, "interval", line_number, positive=True
 )

 for location in (origin, destination):
 if location not in locations:
 locations[location] = None
 adjacency[location] = []

 adjacency[origin].append(
 (destination, edge_type, weight, interval)
 )
 if edge_type == "walk":
 walk_edges.append((origin, destination, weight))

 self._locations = locations
 self._adjacency = adjacency
 self._walk_edges = walk_edges

 # Return True if location is in the map; otherwise return False.
 def inMap(self, location):
 return location in self._locations

 @staticmethod
 def _valid_time(value):
 return (
 isinstance(value, (int, float))
 and not isinstance(value, bool)
 and math.is

[FILE final_project/campus_nav_6ed9446b2307ad30e3f3b16f2739d2b6.py]
import math

import graph


class CampusNav:

 def __init__(self):

 pass


 def read_from_file(self,filename):

 pass


 # return True if location in map, otherwise return False

 def inMap(self, location):

 pass


 def Navigate(self,orig,dest,mtime):


 return total_time, path


 # return minimum cost deployment map

 # a list of edges. each edge: (orig, dest, weight)

 def FiberOptic_deployment(self):


 return edge_list


def main_menu(campus):

 """

 Runs the interactive Console User Interface for the Campus System.

 Expects an initialized CampusGraph object as input.

 """

 while True:

 print("\n" + "=" * 50)

 print(" Welcome to Campus Transit & Navigation System")

 print("=" * 50)

 print("1. Find Fastest Route (Time-Dependent Dijkstra)")

 print("2. Generate Fiber Optic Network Layout (Kruskal MST)")

 print("3. Exit System")

 print("-" * 50)


 choice = input("Select an option (1-3): ").strip()


 # ---------------------------------------------------------

 # OPTION 1: TIME-DEPENDENT DIJKSTRA NAVIGATION

 # ---------------------------------------------------------

 if choice == '1':

 print("\n--- Route Planning Mode ---")

 start_node = input("Enter Starting Point: ").strip()

 end_node = input("Enter Destination: ").strip()


 # Validation: Check if buildings exist in the graph database

 if not campus.inMap(start_node) or not campus.inMap(end_node):

 print("❌ Error: One or both buildings do not exist in the campus database.")

 continue


 time_input = input("Enter Departure Time (minutes from 08:00, e.g., 0): ").strip()


 # Validation: Check if time input is a valid non-negative integer

 if not time_input.isdigit():

 print("❌ Error: Departure time must be a valid non-negative number.")

 continue


 start_time = int(time_input)


 print("\n🔄 Calculating optimal route...")

 arrival_time, path = campus.Navigate(start_node, end_node, start_time)


 if arrival_time is None or arrival_time == float('inf'):

 print(f"❌ No route could be found connecting '{start_node}' to '{end_node}'.")

 else:

 # Calculate absolute clock time for presentation

 total_minutes = 8 * 60 + arrival_time # 08:00 in minutes + elapsed minutes

 hours = (total_minutes // 60) % 24

 mins = total_minutes % 60


 print("\nSuccess! Fastest Route Found:")

 print("-" * 50)

 print(f"Path: {' ➔ '.join(path)}")

 print(f"Total Travel Time: {arrival_time - start_time} minutes")

 print(f"Estimated Arrival: {hours:02d}:{mins:02d}")

 print("-" * 50)


 # ---------------------------------------------------------

 # OPTION 2: FIBER DEPLOYMENT

 # ---------------------------------------------------------

 elif choice == '2':

 print("\n--- Fiber Optic Network Deployment Report ---")

 print("Constructing Minimun cost map...\n")


 min_edges = campus.FiberOptic_deployment()


 if not min_edges:

 print("❌ Error: Could not generate network layout. Graph might be completely disconnected.")

 else:

 print("Recommended Trenching Layout:")

 total_cost = 0

 # Expecting mst_edges to return tuples of (u, v, weight)

 for u, v, weight in min_edges:

 print(f" • {u} ➔ {v} (Cost: {weight})")

 total_cost += weight


 print("-" * 50)

 print(f"Total Network Infrastructure Cost: {total_cost} units")

 print("-" * 50)


 # ---------------------------------------------------------

 # OPTION 3: EXIT PROGRAM

 # ---------------------------------------------------------

 elif choice == '3':

 print("\nThank you for using Campus Smart Infrastructure. Exiting system... Goodbye!")

 break


 # ---------------------------------------------------------

 # INVALID INPUT HANDLING

 # ---------------------------------------------------------

 else:

 print("❌ Invalid selection. Please enter a number between 1 and 3.")


if __name__ == "__main__":

 campus = CampusNav()

 campus.read_from_file("campus_nav.csv")

 main_menu(campus)


[FILE final_project/code_tester.py]
"""Corrected sanity tests for the Campus Transit & Navigation System."""

from pathlib import Path

from campus_nav import CampusNav

def run_sanity_tests():
 folder = Path(__file__).parent
 campus = CampusNav()
 campus.read_from_file(folder / "campus_map_testcase1.csv")

 tests = []

 arrival, path = campus.Navigate("MainGate", "Lab", 0)
 tests.append(
 (
 "navigation at 08:00",
 arrival == 6 and path == ["MainGate", "Library", "Lab"],
 )
 )

 arrival, path = campus.Navigate("MainGate", "Library", 3)
 tests.append(
 (
 "navigation at 08:03",
 arrival == 12 and path == ["MainGate", "Library"],
 )
 )

 fiber = campus.FiberOptic_deployment()
 tests.append(
 (
 "walk-only fiber MST",
 len(fiber) == 3
 and all(len(edge) == 3 for edge in fiber)
 and sum(edge[2] for edge in fiber) == 15,
 )
 )

 print("=" * 56)
 print("Campus System Sanity Tests")
 print("=" * 56)
 for name, passed in tests:
 print(f"{'PASS' if passed else 'FAIL'}: {name}")

 if not all(passed for _, passed in tests):
 raise AssertionError("one or more sanity tests failed")
 print("All sanity tests passed")

if __name__ == "__main__":
 run_sanity_tests()

[FILE final_project/code_tester_ee92eb2f2432e9f9b7321bec6eaf1708.py]
from campus_nav import *

def run_sanity_tests():

 print("=" * 50)

 print("Running Official Campus System Sanity Tests...")

 print("=" * 50)


 # 1. Initialize Graph or map

 campus = CampusNav()


 campus.read_from_file("campus_map_testcase1.csv")


 # ---------------------------------------------------------

 # Test Case A: Navigation at 08:00 (Time = 0)

 # Expected: Fast shuttle available immediately at min 0.

 # Wait time: 0. Travel time: 2. Reach Library at min 2. Walk to Lab (+4) -> total 6.

 # ---------------------------------------------------------

 print("\n[Test 1] Navigation at 08:00 (Start Time = 0)...")

 # navigate from MainGate to the Lab starting at 0 minutes

 ans_time_1, ans_path_1 = campus.Navigate('MainGate', 'Lab', 0)


 expected_time_1 = 6

 expected_path_1 = ['MainGate', 'Library', 'Lab'] # us


 if ans_time_1 == expected_time_1 and ans_path_1 == expected_path_1:

 print("✅ PASS: Correctly optimized utilizing the immediate shuttle!")

 else:

 print(f"❌ FAIL: Expected time {expected_time_1} and path {expected_path_1}")

 print(f" Got time {ans_time_1} and path {ans_path_1}")


 # ---------------------------------------------------------

 # Test Case B: Navigation at 08:03 (Time = 3)

 # Expected: Shuttle missed. Next shuttle at min 10 (Wait 7 mins).

 # Travel time: 2. Reach Library at min 12.

 # Note: Walking to Library takes 5+6=11 mins, arriving earlier!

 # Path should switch to walk: MainGate -> BuildingA -> Library.

 # ---------------------------------------------------------

 print("\n[Test 2] Navigation at 08:03 (Start Time = 3)...")

 ans_time_2, ans_path_2 = campus.Navigate('MainGate', 'Library', 3)


 expected_time_2 = 14 # Start at 3 + 5 (to BuildingA) + 6 (to Library) = 14

 expected_path_2 = ['MainGate', 'BuildingA', 'Library']


 if ans_time_2 == expected_time_2 and ans_path_2 == expected_path_2:

 print("✅ PASS: Correctly dynamically switched to walking paths to avoid shuttle delay!")

 else:

 print(f"❌ FAIL: Expected time {expected_time_2} and path {expected_path_2}")

 print(f" Got time {ans_time_2} and path {ans_path_2}")


 # ---------------------------------------------------------

 # Test Case C: Fiber Optic Network

 # Expected connections: (MainGate-BuildingA: 5), (Library-Lab: 4), (BuildingA-Library: 6)

 # Total Cost = 5 + 4 + 6 = 15. Shuttle edge must be completely ignored.

 # ---------------------------------------------------------

 print("\n[Test 3] Fiber Deployment (Walk Paths Only)...")

 fiber_connections = campus.FiberOptic_deployment()


 # Calculate total weight of returned MST

 total_cost = sum(edge[2] for edge in fiber_connections) if fiber_connections else 0

 shuttle_included = any(edge[3] == 'shuttle' for edge in fiber_connections) if fiber_connections else False


 if total_fiber_cost == 15 and not shuttle_included and len(fiber_connections) == 3:

 print("✅ PASS: successfully built using only walk edges with minimal cost of 15!")

 else:

 print(f"❌ FAIL: Expected total cost 15 with 3 walk edges.")

 print(f" Got total cost {total_cost}, total edges {len(fiber_connections) if fiber_connections else 0}")

 if shuttle_included:

 print(" CRITICAL ERROR: Shuttle edges were incorrectly included in the fiber network!")


 print("\n" + "=" * 50)

 print("Sanity Check Simulation Finished.")

 print("=" * 50)


if __name__ == "__main__":

 run_sanity_tests()


[FILE final_project/test_campus_nav.py]
import io
import csv
import heapq
import itertools
import math
import random
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from campus_nav import CampusNav, MinHeap, UnionFind, main_menu

HERE = Path(__file__).parent

def assert_heap_invariant(heap):
 assert heap.heapList[0] is None
 assert heap.currentSize == len(heap.heapList) - 1
 for child in range(2, heap.currentSize + 1):
 parent = child // 2
 assert heap.heapList[parent][:2] <= heap.heapList[child][:2]

def test_heap():
 heap = MinHeap()
 assert heap.is_empty()
 for key, value in [(5, "five"), (1, "first"), (3, "three"), (1, "second")]:
 heap.insert(key, value)
 assert_heap_invariant(heap)

 output = []
 while not heap.is_empty():
 output.append(heap.remove_min())
 assert_heap_invariant(heap)
 assert output == [(1, "first"), (1, "second"), (3, "three"), (5, "five")]

 try:
 heap.remove_min()
 except IndexError:
 pass
 else:
 raise AssertionError("empty heap removal must fail")

 rng = random.Random(1701)
 heap = MinHeap()
 expected = []
 for order in range(2_000):
 key = rng.randint(-50, 50)
 value = (key, order)
 heap.insert(key, value)
 expected.append(value)
 assert_heap_invariant(heap)
 actual = []
 while not heap.is_empty():
 actual.append(heap.remove_min()[1])
 assert_heap_invariant(heap)
 assert actual == sorted(expected, key=lambda item: (item[0], item[1]))

def test_union_find():
 sets = UnionFind("abcde")
 assert sets.union("a", "b")
 assert sets.union("c", "d")
 assert sets.union("a", "c")
 assert sets.find("a") == sets.find("d")
 assert sets.find("a") != sets.find("e")
 assert not sets.union("b", "d")

def test_official_map():
 campus = CampusNav()
 campus.read_from_file(HERE / "campus_map_testcase1.csv")

 assert campus.inMap("MainGate")
 assert campus.inMap("Lab")
 assert not campus.inMap("Missing")

 assert campus.Navigate("MainGate", "Lab", 0) == (
 6,
 ["MainGate", "Library", "Lab"],
 )
 assert campus.Navigate("MainGate", "Library", 3) == (
 12,
 ["MainGate", "Library"],
 )
 assert campus.Navigate("MainGate", "Library", 9) == (
 12,
 ["MainGate", "Library"],
 )
 assert campus.Navigate("Library", "Library", 7) == (7, ["Library"])
 assert campus.Navigate("Library", "MainGate", 0) == (math.inf, [])
 assert campus.Navigate("Missing", "Lab", 0) == (math.inf, [])

 for invalid_time in (-1, math.inf, float("nan"), "0", True):
 try:
 campus.Navigate("MainGate", "Lab", invalid_time)
 except ValueError:
 pass
 else:
 raise AssertionError(f"invalid time was accepted: {invalid_time!r}")

 fiber = campus.FiberOptic_deployment()
 assert len(fiber) == 3
 assert all(len(edge) == 3 for edge in fiber)
 assert sum(edge[2] for edge in fiber) == 15
 assert set(fiber) == {
 ("Library", "Lab", 4),
 ("MainGate", "BuildingA", 5),
 ("BuildingA", "Library", 6),
 }

def test_full_map():
 campus = CampusNav()
 campus.read_from_file(HERE / "campus_map.csv")

 fiber = campus.FiberOptic_deployment()
 assert len(fiber) == 11
 assert sum(edge[2] for edge in fiber) == 59

 assert campus.Navigate("MainGate", "Library", 0) == (
 4,
 ["MainGate", "Library"],
 )
 assert campus.Navigate("MainGate", "Dormitories_North", 0) == (
 15,
 ["MainGate", "Science_Tower", "Dormitories_North"],
 )
 assert campus.Navigate("MainGate", "Dormitories_North", 7) == (
 33,
 ["MainGate", "Library", "Medical_Clinic", "Dormitories_North"],
 )
 assert campus.Navigate("Dormitories_North", "MainGate", 3) == (
 35,
 [
 "Dormitories_North",
 "Medical_Clinic",
 "Library",
 "Computer_Labs",
 "Engineering_Block",
 "Administration",
 "MainGate",
 ],
 )

def write_csv(folder, name, contents):
 path = folder / name
 path.write_text(contents, encoding="utf-8")
 return path

def test_validation_and_disconnected_graph():
 with tempfile.TemporaryDirectory() as temp_name:
 folder = Path(temp_name)
 valid = write_csv(
 folder,
 "valid.csv",
 "orig,dest,type,weight,interval\nA,B,walk,2,\n",
 )
 invalid = write_csv(
 folder,
 "invalid.csv",
 "orig,dest,type,weight,interval\nA,B,shuttle,2,\n",
 )
 disconnected = write_csv(
 folder,
 "disconnected.csv",
 "orig,dest,type,weight,interval\n"
 "A,B,walk,1,\n"
 "C,D,walk,1,\n",
 )

 campus = CampusNav()
 campus.read_from_file(valid)
 assert campus.Navigate("A", "B", 0) == (2, ["A", "B"])

 try:
 campus.read_from_file(invalid)
 except ValueError:
 pass
 else:
 raise AssertionError("missing shuttle interval was accepted")

 # A failed load must not destroy the map that was already loaded.
 assert campus.Navigate("A", "B", 0) == (2, ["A", "B"])

 campus.read_from_file(disconnected)
 assert campus.FiberOptic_deployment() == []
 assert campus.Navigate("A", "D", 0) == (math.inf, [])

 invalid_cases = {
 "missing_header.csv": "A,B,walk,2,\n",
 "unknown_type.csv": (
 "orig,dest,type,weight,interval\nA,B,train,2,5\n"
 ),
 "negative_weight.csv": (
 "orig,dest,type,weight,interval\nA,B,walk,-1,\n"
 ),
 "zero_interval.csv": (
 "orig,dest,type,weight,interval\nA,B,shuttle,2,0\n"
 ),
 "nonnumeric.csv": (
 "orig,dest,type,weight,interval\nA,B,walk,fast,\n"
 ),
 }
 for name, contents in invalid_cases.items():
 path = write_csv(folder, name, contents)
 try:
 CampusNav().read_from_file(path)
 except ValueError:
 pass
 else:
 raise AssertionError(f"invalid CSV was accepted: {name}")

def test_console_menu():
 campus = CampusNav()
 campus.read_from_file(HERE / "campus_map_testcase1.csv")
 answers = ["1", "MainGate", "Lab", "0", "2", "3"]
 output = io.StringIO()
 with patch("builtins.input", side_effect=answers), redirect_stdout(output):
 main_menu(campus)

 text = output.getvalue()
 assert "Path: MainGate -> Library -> Lab" in text
 assert "Total Travel Time: 6 minutes" in text
 assert "Estimated Arrival: 08:06" in text
 assert "Total Network Infrastructure Cost: 15 units" in text
 assert "Goodbye" in text

def test_console_validation():
 camp

[FILE final_project/דוגמאות למיונים/bubble_sort_4e2d9dd39fd492e0479ac5c568a49c5f.py]
import random

import time


# L stands for any mutable object that has an array interface

# Like a standard Python list for example

# For simplicity, L is assumed to be a list of integers, but the algorithm

# applies to any object that also implements the comparison operators: '<',

# '>', '==', '<=', '>='


# L is a list of integers that we want to sort

def bubble_sort(L):

 N = len(L)

 while True:

 sorted = True

 for i in range(0,N-1):

 if L[i+1] < L[i]:

 sorted = False

 L[i], L[i+1] = L[i+1], L[i]

 if sorted:

 return


# This is slightly different but simpler version which is also called bubble sort

# L is a list of integers that we want to sort

def bubble_sort2(L):

 N = len(L)

 for i in range(0,N-1):

 for j in range(i+1, N):

 if L[j] < L[i]:

 L[i], L[j] = L[j], L[i]


def bubble_sort_test():

 for i in range(10):

 L = range(0,10)

 random.shuffle(L)

 print "L = ", L

 bubble_sort(L)

 print "Bubble sort:", L

 raw_input("Press any key to continue:")


def bubble_sort_slow_motion(N=10):

 L = range(0,N)

 random.shuffle(L)

 stage = 0

 while True:

 print "STAGE %d: %s" % (stage, L)

 stage += 1

 sorted = True

 for i in range(0,N-1):

 if L[i+1] < L[i]:

 sorted = False

 L[i], L[i+1] = L[i+1], L[i]


 if sorted:

 return


def bubble_sort_runtime_graph():

 import matplotlib.pyplot as pyplot

 import sys

 #sys.path.append("d:/python") # private library (Samy)

 #from html_utils import * # Will try to release it later

 Sizes = [100*i for i in range(1,30)]

 Times = list()

 for N in Sizes:

 print "N=", N

 t = bubble_sort_average_time(N,3)

 t = round(t,4)

 Times.append(t)


 pyplot.plot(Sizes, Times)

 pyplot.xlabel('List Size')

 pyplot.ylabel('Run Time')

 pyplot.show()

 #header = ('List Size', 'Run Time (seconds)')

 #html_table("d:/dropbox/public/table.html", header, [Sizes, Times])


# Create num_tests lists of size list_size and compute

# average time for doing bubble_sort on these lists

def bubble_sort_average_time(list_size, num_tests):

 times = list()

 L = range(0, list_size)


 for i in range(num_tests):

 random.shuffle(L)

 t0 = time.time()

 bubble_sort(L)

 t1 = time.time()

 t = t1-t0

 times.append(t)


 return sum(times)/num_tests


if __name__ == "__main__":

 #bubble_sort_test()

 #bubble_sort_slow_motion(10)

 bubble_sort_runtime_graph()


[FILE final_project/דוגמאות למיונים/radix_sort_057a5d01ee0b794c32bbefe97c87ad4a.py]
# L stands for any mutable object that has an array interface

# Like a standard Python list for example

# For simplicity, L is assumed to be a list of integers, but the algorithm

# applies to any object that also implements the comparison operators: '<',

# '>', '==', '<=', '>='


def radix_sort(L):

 RADIX = 10

 maxLength = False

 tmp , placement = -1, 1


 while not maxLength:

 maxLength = True

 # declare and initialize buckets

 buckets = [list() for i in range( RADIX )]


 # split L between lists

 for i in L:

 tmp = i / placement

 buckets[tmp % RADIX].append(i)

 if maxLength and tmp > 0:

 maxLength = False


 # empty lists into L array

 a = 0

 for b in range(RADIX):

 buck = buckets[b]

 for i in buck:

 L[a] = i

 a += 1


 # move to next digit

 placement *= RADIX


[FILE final_project/דוגמאות למיונים/selection_sort_9fccb86419a618615c72856db0a0e1c0.py]
import random

import time


# L stands for any mutable object that has an array interface

# Like a standard Python list for example

# For simplicity, L is assumed to be a list of integers, but the algorithm

# applies to any object that also implements the comparison operators: '<',

# '>', '==', '<=', '>='


def selection_sort(L):

 n = len(L)

 for i in range(0, n):

 min = i # min = index of minimal element in L[i],L[i+1], ..., L[n-1]

 for j in range(i + 1, n):

 if L[j] < L[min]:

 min = j

 L[i], L[min] = L[min], L[i] # swap


def sort_test(sorter):

 for i in range(10):

 L = range(0,10)

 random.shuffle(L)

 print "L = ", L

 sorter(L)

 print "sorted list", L

 raw_input("Press any key to continue:")


def selection_sort_slow_motion(n=10):

 L = range(0,n)

 random.shuffle(L)

 print L

 stage = 0

 for i in range(0, n):

 min = i

 for j in range(i + 1, n):

 if L[j] < L[min]:

 line = "STAGE %d: %s :" % (stage, L)

 stage += 1

 raw_input(line)

 min = j

 L[i], L[min] = L[min], L[i] # swap


#import sys

#sys.path.append("d:/python") # private library (Samy)

#from html_utils import * # Will try to release it later

def sort_runtime_graph(sorter):

 import matplotlib.pyplot as pyplot

 import sys

 Sizes = [100*i for i in range(1,30)]

 Times = list()

 for N in Sizes:

 print "N=", N

 t = sort_average_time(sorter, N,16)

 t = round(t,4)

 Times.append(t)


 pyplot.plot(Sizes, Times)

 pyplot.xlabel('List Size')

 pyplot.ylabel('Run Time')

 pyplot.show()

 #header = ('List Size', 'Run Time (seconds)')

 #html_table("d:/dropbox/public/table.html", header, [Sizes, Times])


# Create num_tests lists of size list_size and compute

# average time for doing sort on these lists

def sort_average_time(sorter, list_size, num_tests):

 times = list()

 L = range(0, list_size)


 for i in range(num_tests):

 random.shuffle(L)

 t0 = time.time()

 sorter(L)

 t1 = time.time()

 t = t1-t0

 times.append(t)


 return sum(times)/num_tests


if __name__ == "__main__":

 #sort_test(selection_sort)

 #selection_sort_slow_motion(10)

 sort_runtime_graph(selection_sort)


[FILE final_project/דוגמאות למיונים/sort_bench_6b7f69325099faf706526430a8b062a9.py]
import random

import time

#import sys

#sys.path.append("d:/python") # private library (Samy)

#from html_utils import * # Will try to release it later


def sort_test(sorter):

 for i in range(10):

 L = range(0,10)

 random.shuffle(L)

 print "L = ", L

 sorter(L)

 print "sorted list", L

 raw_input("Press any key to continue:")


def sort_runtime_graph(sorter, n=10):

 import matplotlib.pyplot as pyplot

 import sys

 Sizes = [100*i for i in range(1,n)]

 Times = list()

 for N in Sizes:

 print "N=", N

 t = sort_average_time(sorter, N, 16)

 t = round(t,4)

 Times.append(t)


 pyplot.plot(Sizes, Times)

 pyplot.xlabel('List Size')

 pyplot.ylabel('Run Time')

 pyplot.show()

 #header = ('List Size', 'Run Time (seconds)')

 #html_table("d:/dropbox/public/table.html", header, [Sizes, Times])


# Create num_tests lists of size list_size and compute

# average time for doing sort on these lists

def sort_average_time(sorter, list_size, num_tests):

 times = list()

 L = range(0, list_size)


 for i in range(num_tests):

 random.shuffle(L)

 t0 = time.time()

 sorter(L)

 t1 = time.time()

 t = t1-t0

 times.append(t)


 return sum(times)/num_tests
