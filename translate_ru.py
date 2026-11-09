"""Make the Russian deck (deck_ru/) from the built English deck (deck_en/index.html).

Usage: python3 build.py en && python3 translate_ru.py
The Russian version intentionally has no Elbit mention and no GPS-jamming / drone-warfare framing.
"""
import pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).parent
src = (ROOT / "deck_en/index.html").read_text(encoding="utf-8")
out = ROOT / "deck_ru"
if not out.exists():
    shutil.copytree(ROOT / "deck_en", out, ignore=shutil.ignore_patterns("index.html", "thumbs"))
for sub in ("assets", "fonts"):
    shutil.copytree(ROOT / "deck_en" / sub, out / sub, dirs_exist_ok=True)
for f in ("remote.html",):
    shutil.copy(ROOT / "deck_en" / f, out / f)

T = [
# ---------- speaker notes (long first) ----------
("Ateno builds a dedicated chip that lets autonomous systems build 3D maps on board and navigate without GPS. The chip on screen is a concept render, not silicon.",
 "Ateno делает специализированный чип, который позволяет автономным системам строить 3D-карты на борту и ориентироваться без GPS. Чип на экране — концепт-рендер, не кремний."),
("GPS answers the question until it doesn't: it can be denied, faked, or never there. And there is often no link to send data anywhere. The machine has to build a 3D map from its own cameras, while it moves, and locate itself in it.",
 "GPS отвечает на этот вопрос, пока он доступен. Часто его нет, а связи с сервером тоже нет. Машина должна строить 3D-карту по своим камерам, на ходу, и находить себя на ней."),
("Gaussian Splatting builds photorealistic maps from ordinary cameras. But building one is a training job. Sources: published Gaussian SLAM benchmarks; 30+ practitioner interviews since May 2026.",
 "Gaussian Splatting строит фотореалистичные карты по обычным камерам. Но построение карты — это обучение. Источники: опубликованные бенчмарки Gaussian SLAM; 30+ интервью с практиками с мая 2026."),
("We profiled the reference pipeline (gsplat on an NVIDIA L4) before writing any RTL. Building the map is training, and training is where the compute goes. Most accelerators stop at rendering.",
 "Мы профилировали эталонный пайплайн (gsplat на NVIDIA L4) до того, как написали RTL. Построение карты — это обучение, и туда уходят вычисления. Большинство ускорителей ограничиваются рендерингом."),
("Ateno AX is one chip for one workload: it trains the 3D map and renders it, on the device, with no connection. The chip image is a concept render, not silicon. Be precise about what exists: rendering and training run on our FPGA prototype; camera poses are still computed in software.",
 "Ateno AX — один чип для одной задачи: он обучает 3D-карту и рендерит её на устройстве, без связи. Изображение чипа — концепт-рендер. Точно о том, что есть: рендеринг и обучение работают на нашем FPGA-прототипе; позы камер пока считаются программно."),
("Full 1080p rendering ran end to end on an AWS F2 FPGA, September 2026. The build-up animation is illustrative; the final frame is the FPGA output. If asked about GPUs: today the FPGA is about 70x slower than an NVIDIA L4 on this frame (262 ms vs about 3.7 ms). What carries over to silicon is the cycle count, not FPGA wall-clock.",
 "Полный рендеринг 1080p прошёл целиком на FPGA AWS F2, сентябрь 2026. Анимация сборки иллюстративна, финальный кадр — вывод FPGA. Если спросят про GPU: сегодня FPGA примерно в 70 раз медленнее NVIDIA L4 на этом кадре (262 мс против ~3,7 мс). В кремний переносится число тактов, а не время на FPGA."),
("Same scene, same resolution. 1.02 s on August 31, 262 ms on September 10: 3.9 times faster. Not fast yet: the next slide shows exactly where the time goes.",
 "Та же сцена, то же разрешение. 1,02 с 31 августа, 262 мс 10 сентября: в 3,9 раза быстрее. Пока не быстро: следующий слайд показывает, куда уходит время."),
("This is our own bottleneck on the FPGA, not a GPU problem: on GPUs, sorting is about 12% of training time. Fixing our sorting engine is the next step. The milliseconds are simply the percentages applied to 262 ms.",
 "Это наше узкое место на FPGA, а не проблема GPU: на GPU сортировка — около 12% времени обучения. Следующий шаг — ускорить блок сортировки. Миллисекунды — это проценты от 262 мс."),
("This is the standard Gaussian Splatting training step: render, compare with the camera frame, backpropagate, update. All four stages run on our FPGA prototype. The 13x figure is the Adam step benchmarked on a single Gaussian (51 microseconds vs 665 on CPU). Next: large scenes and energy efficiency.",
 "Это стандартный шаг обучения 3DGS: рендер, сравнение с кадром камеры, обратный проход, обновление. Все четыре этапа работают на нашем FPGA-прототипе. 13× — шаг Adam, измеренный на одном гауссиане (51 мкс против 665 на CPU). Дальше: большие сцены и энергоэффективность."),
("Tape-out is gated on Phase 2 results. Do not promise a silicon date.", "Tape-out зависит от результатов второй фазы. Не обещать дату кремния."),
("2.8M times 20% times $300 is about $170M; times $1,000 is about $560M. Drones, other autonomous systems and IP royalties are upside on top.",
 "2,8 млн × 20% × $300 ≈ $170 млн; × $1 000 ≈ $560 млн. Дроны, другие автономные системы и роялти за IP — дополнительный потенциал."),
("GPS-denied, disconnected operation is the common thread. Drones and ground robots increasingly have to map and localize on board, with no GPS and no link. Elbit Systems' engineering leadership sees strong potential and is interested as we mature; our current stage is early for them. Name Elbit only with their OK.",
 "Общая нить — работа без GPS и без связи: машинам нужно строить карту и находить себя на ней прямо на борту."),
("We start with paid design partnerships, which fund the engineering and validate demand before silicon.", "Начинаем с платных дизайн-партнёрств: они финансируют разработку и подтверждают спрос до кремния."),
("Edge-AI NPU companies accelerate neural nets, so they are potential partners rather than competitors.", "Компании edge-AI NPU ускоряют нейросети, поэтому они скорее партнёры, чем конкуренты."),
("Be honest about the stage: interest and an unpaid pilot, not contracts. Elbit: strong interest in the technology, but our stage is early for them; no commitment.",
 "Честно о стадии: интерес и неоплачиваемый пилот, а не контракты. Не называть компанию до её согласия."),
("Rendering and training paths were built in about five months, June to October 2026, by the two of us.", "Рендеринг и обучение мы вдвоём построили примерно за пять месяцев, с июня по октябрь 2026."),
("We are raising $1.25M pre-seed. Be ready to say what it buys and for how long: the three milestones on this slide, and the runway in months.",
 "Привлекаем $1,25 млн pre-seed. Будь готов сказать, на что пойдут деньги и на сколько месяцев их хватит: три вехи на этом слайде."),
("<aside>Thank you.</aside>", "<aside>Спасибо.</aside>"),
# ---------- cover ----------
("Navigation that doesn't<br>depend on GPS", "Навигация,<br>не зависящая от GPS"),
("Sviatoslav Gladyshev · Co-founder &amp; CEO · info@ateno.co · Pre-seed · November 2026", "Святослав Гладышев · сооснователь и CEO · info@ateno.co · Pre-seed · ноябрь 2026"),
(">Concept render<", ">Концепт-рендер<"),
# ---------- eyebrows ----------
("</span> The problem</p>", "</span> Проблема</p>"), ("</span> Today</p>", "</span> Сегодня</p>"), ("</span> Our insight</p>", "</span> Наш инсайт</p>"),
("</span> The product</p>", "</span> Продукт</p>"), ("</span> What already runs</p>", "</span> Что уже работает</p>"), ("</span> Progress</p>", "</span> Прогресс</p>"),
("</span> Where the time goes</p>", "</span> Куда уходит время</p>"), ("</span> Training in hardware</p>", "</span> Обучение в железе</p>"),
("</span> Roadmap</p>", "</span> Дорожная карта</p>"), ("</span> Market</p>", "</span> Рынок</p>"), ("</span> Applications</p>", "</span> Применения</p>"),
("</span> Business model</p>", "</span> Бизнес-модель</p>"), ("</span> Landscape</p>", "</span> Конкуренты</p>"), ("</span> Traction</p>", "</span> Тракшн</p>"),
("</span> Team</p>", "</span> Команда</p>"), ("</span> The ask</p>", "</span> Раунд</p>"),
# ---------- problem ----------
("Every autonomous system asks:", "Каждая автономная система спрашивает:"), ("where am I?", "где я?"),
(">Denied<", ">Без GPS<"), ("GPS can be jammed, spoofed or simply absent.", "Сигнал слабый, отражённый или его нет совсем."),
(">Underground and indoors<", ">Под землёй и в зданиях<"), ("Tunnels, mines and buildings have no signal at all.", "В тоннелях, шахтах и зданиях сигнала нет."),
(">Disconnected<", ">Без связи<"), ("No reliable link to a server. The map has to be built on board.", "Надёжной связи с сервером нет. Карту нужно строить на борту."),
# ---------- today ----------
("The best 3D maps come from Gaussian Splatting.", "Лучшие 3D-карты дают гауссовы сплаты (3DGS)."),
("Building one takes a datacenter GPU.", "Но для их построения нужен GPU из дата-центра."),
("3DGS scene, shown in a software viewer", "3DGS-сцена в программном вьюере"),
(">0.4–5 FPS<", ">0,4–5 к/с<"), ("Published Gaussian SLAM on NVIDIA Jetson. Too slow to navigate with.", "Опубликованные Gaussian SLAM на NVIDIA Jetson. Слишком медленно для навигации."),
(">4–24 h<", ">4–24 ч<"), ("To reconstruct a large scene on GPUs. Record now, map later.", "На реконструкцию большой сцены на GPU. Запись сейчас, карта потом."),
(">20–80 GB<", ">20–80 ГБ<"), ("GPU memory for large scenes. Nothing on board comes close.", "Видеопамяти для больших сцен. Бортовое железо и близко не подходит."),
# ---------- insight ----------
("A robot doesn't need to view a map.", "Роботу не нужно смотреть на карту."), ("It needs to build one.", "Ему нужно её построить."),
("of 3DGS training time is the backward pass and optimizer. Our hardware is designed around it.", "времени обучения 3DGS уходит на обратный проход и оптимизатор. Наше железо спроектировано вокруг этого."),
# ---------- product ----------
("One chip that builds the map and renders it.<br>On the device, offline.", "Один чип строит карту и рендерит её.<br>На устройстве, без связи."),
(">Input<", ">Вход<"), ("Frames from the robot's own cameras", "Кадры с собственных камер робота"),
(">Builds<", ">Строит<"), ("A 3D Gaussian map, trained on the chip", "3D-карту из гауссиан, обучаемую на чипе"),
(">Renders<", ">Рендерит<"), ("Photorealistic views, 1080p today", "Фотореалистичные виды, сейчас 1080p"),
(">Link<", ">Связь<"), ("None needed. Nothing leaves the device", "Не нужна. Данные не покидают устройство"),
(">Ships as<", ">Формат<"), ("Compute module, or IP block in an SoC", "Модуль или IP-блок внутри SoC"),
(">Poses<", ">Позы камер<"), ("Software today (COLMAP); on-chip next", "Сейчас программно (COLMAP); на чипе — дальше"),
(">Status<", ">Статус<"), ("Rendering and training run on FPGA", "Рендеринг и обучение работают на FPGA"),
# ---------- proof ----------
("Illustrative build-up. The final frame is our FPGA render (AWS F2).", "Сборка иллюстративна. Финальный кадр — наш рендер на FPGA (AWS F2)."),
("This frame was rendered by our hardware.", "Этот кадр отрендерило наше железо."),
(">173,161</span>", ">173 161</span>"), (">2,073,600</span>", ">2 073 600</span>"),
(">Gaussians in the scene<", ">гауссиан в сцене<"), (">pixels, computed by our design<", ">пикселей посчитал наш дизайн<"),
(">end to end on the FPGA<", ">целиком на FPGA<"), (">Closed<", ">Закрыт<"), (">timing on AWS F2<", ">тайминг на AWS F2<"),
# ---------- speed ----------
("From one second to 262 ms.", "С одной секунды до 262 мс."), ("In ten days.", "За десять дней."),
(">3.9×<", ">3,9×<"), ("faster frame time, same 1080p scene,<br>173,161 Gaussians, FPGA core at 100 MHz.", "быстрее кадр: та же сцена 1080p,<br>173 161 гауссиан, ядро FPGA на 100 МГц."),
(">1.02 s<", ">1,02 с<"), (">262 ms<", ">262 мс<"), (">Aug 31<", ">31 авг<"), (">Sep 10<", ">10 сен<"),
("Not fast yet, and we know exactly why: next slide.", "Пока не быстро, и мы точно знаем почему: следующий слайд."),
# ---------- bottleneck ----------
("Three quarters of every frame is sorting.", "Три четверти каждого кадра — сортировка."), ("That's what we fix next.", "Это мы чиним следующим."),
(">262 ms</p>", ">262 мс</p>"), (">per 1080p frame<", ">на кадр 1080p<"), (">Sorting<", ">Сортировка<"), (">Frontend<", ">Фронтенд<"), (">Render<", ">Рендер<"),
("· ≈197 ms", "· ≈197 мс"), ("· ≈50 ms", "· ≈50 мс"), ("· ≈16 ms", "· ≈16 мс"),
("Measured on our FPGA (1080p, 100 MHz); ms = share of 262 ms. Our own bottleneck, not a GPU one.", "Измерено на нашей FPGA (1080p, 100 МГц); мс — доля от 262 мс. Наше узкое место, а не GPU."),
# ---------- training ----------
("Most accelerators stop at rendering.", "Другие ускорители умеют только рендер."), ("The whole training loop runs on our FPGA.", "Весь цикл обучения работает на нашем FPGA."),
(">Gaussians → image<", ">гауссианы → кадр<"), (">✓ On FPGA<", ">✓ На FPGA<"), (">Compare<", ">Сравнение<"), (">vs the camera frame<", ">с кадром камеры<"),
(">Backward<", ">Backprop<"), (">gradients<", ">градиенты<"), ("zzunused","zzunused"),
(">Adam update<", ">Шаг Adam<"), (">new Gaussians<", ">новые гауссианы<"),
("Repeated thousands of times per scene", "Повторяется тысячи раз на сцену"),
("faster Adam step on FPGA<br>vs our CPU reference (1 Gaussian)", "быстрее шаг Adam на FPGA<br>против нашей CPU-версии (1 гауссиан)"),
("tests passing<br>in our regression suite", "тестов проходят<br>в регрессионном наборе"),
("claims in our UAE<br>patent application", "пунктов в нашей<br>патентной заявке в ОАЭ"),
# ---------- roadmap ----------
("FPGA proof first.", "Сначала доказательство на FPGA."), ("Silicon only after.", "Кремний — только потом."),
(">Done · Jun–Nov 2026<", ">Сделано · июнь–нояб 2026<"), (">Working prototype<", ">Рабочий прототип<"),
("1080p rendering and full training on FPGA. 723 tests passing.", "Рендеринг 1080p и полное обучение на FPGA. 723 теста проходят."),
(">This round<", ">Этот раунд<"), (">Scale and efficiency<", ">Масштаб и эффективность<"),
("Large, real-world scenes. Energy benchmark vs Jetson and GPU.", "Большие реальные сцены. Бенчмарк энергии против Jetson и GPU."),
(">After proof<", ">После доказательства<"), (">Silicon<", ">Кремний<"),
("Pick the process node from measured needs. Tape out with design partners.", "Выбор техпроцесса по измеренным требованиям. Tape-out с дизайн-партнёрами."),
("No tape-out until performance, power and economics are proven on the FPGA.", "Никакого tape-out, пока производительность, энергопотребление и экономика не доказаны на FPGA."),
# ---------- market ----------
("Every robot that moves", "Каждому движущемуся роботу"), ("needs to see in 3D.", "нужно видеть в 3D."),
(">2.8M<", ">2,8 млн<"), ("mobile robots shipped per year by 2030<br>(ABI Research)", "мобильных роботов в год к 2030<br>(ABI Research)"),
(">$170–560M<", ">$170–560 млн<"), ("per year in modules at 20% adoption and<br>$300–1,000 a unit, from mobile robots alone", "в год на модулях при 20% проникновения и<br>$300–1&#160;000 за штуку, только мобильные роботы"),
("Before drones and other autonomous systems, and IP licensing. A scenario, not a forecast.", "Без учёта дронов, других автономных систем и лицензирования IP. Сценарий, а не прогноз."),
# ---------- applications (civil framing in RU) ----------
("Built for autonomy", "Для автономных машин"), ("where GPS can't be trusted.", "там, где GPS ненадёжен."),
(">Autonomous drones<", ">Дроны в помещениях<"), ("Navigation where GPS is jammed, spoofed or unavailable.", "Полёты внутри зданий, складов и промышленных объектов."),
(">Ground robots<", ">Наземные роботы<"), ("Unmapped or changing terrain, with no link to a server.", "Неизвестная или меняющаяся местность, без связи с сервером."),
(">Critical infrastructure<", ">Инфраструктура<"), ("Security and inspection of sites where data must stay on site.", "Инспекция объектов, где данные должны оставаться на месте."),
(">Tunnels and underground<", ">Тоннели и подземные объекты<"), ("Mines, tunnels and subterranean spaces with no signal at all.", "Шахты, тоннели и подземные пространства без сигнала."),
("Every one of these needs the same thing: a map built on board, in real time, with nothing sent off the device.", "Всем им нужно одно: карта, построенная на борту, в реальном времени, без передачи данных наружу."),
# ---------- model ----------
("Three ways we make money.", "Три источника выручки."),
(">First<", ">Сначала<"), (">Design partnerships<", ">Дизайн-партнёрства<"),
("Drone and robot platform makers fund the engineering to fit the chip to their system. About $120K each.", "Производители дронов и роботов оплачивают адаптацию чипа под свою систему. Около $120 тыс. каждое."),
(">Then<", ">Затем<"), (">Compute modules<", ">Вычислительные модули<"),
("An edge module at $300–1,000 a unit, in every robot that maps.", "Бортовой модуль за $300–1&#160;000 в каждом роботе, который строит карту."),
(">At scale<", ">На масштабе<"), (">IP licensing<", ">Лицензирование IP<"),
("A per-chip royalty for SoC vendors that integrate our block.", "Роялти с каждого чипа для производителей SoC, встраивающих наш блок."),
("No revenue today. Design partnerships are what we sell first.", "Выручки пока нет. Первое, что мы продаём, — дизайн-партнёрства."),
# ---------- competition ----------
("Today's edge chips weren't built", "Сегодняшние edge-чипы не создавались"), ("to make the map.", "для построения карт."),
(">Who<", ">Кто<"), (">What they do<", ">Что делают<"), (">The gap<", ">Чего не хватает<"),
(">General-purpose edge compute<", ">Универсальные edge-вычисления<"), (">0.4–5 FPS on Gaussian SLAM<", ">0,4–5 к/с на Gaussian SLAM<"),
(">Edge-AI NPUs<", ">Edge-AI NPU<"), (">Accelerate neural networks<", ">Ускоряют нейросети<"), (">Not the 3DGS dataflow; partners<", ">Не под поток данных 3DGS; партнёры<"),
(">Academic accelerators<", ">Академические ускорители<"), (">GSCore, StreamingGS and others<", ">GSCore, StreamingGS и другие<"), (">Not products; mostly rendering<", ">Не продукты; в основном рендер<"),
(">Training and rendering in hardware<", ">Обучение и рендер в железе<"), (">Built for the robot<", ">Сделан для робота<"),
# ---------- traction (no Elbit in RU) ----------
("Early, and real.", "Рано, но по-настоящему."), (">Pilot<", ">Пилот<"),
("Research pilot with the S.M.A.R.T. Construction Research Group at NYU Abu Dhabi.", "Исследовательский пилот с группой S.M.A.R.T. Construction Research в NYU Abu Dhabi."),
(">Industry<", ">Индустрия<"),
("Elbit Systems' engineering sees strong potential in our technology.",
 "Крупная технологическая компания видит в нашей технологии сильный потенциал."),
(">Demand<", ">Спрос<"), (">IP<", ">Патент<"), ("Patent application submitted in the UAE, with 20 claims on our hardware.", "Подана патентная заявка в ОАЭ: 20 пунктов формулы на наше железо."), ("30+ practitioner interviews; several said they would pay $3–5K per project.", "30+ интервью с практиками; несколько готовы платить $3–5 тыс. за проект."),
("No revenue or LOI yet. The pilot is unpaid; the willingness to pay is verbal.", "Выручки и LOI пока нет. Пилот неоплачиваемый; готовность платить — устная."),
(">Pre-seed · November 2026<", ">Pre-seed · ноябрь 2026<"),
# ---------- pictures from the website (Nov 2026) ----------
(" The three pictures are illustrations from our website, not field footage.", " Три картинки — иллюстрации с нашего сайта, не съёмка."),
(" The map pictures are simulated scenes from our website.", " Карты на картинках — симуляции с нашего сайта."),
(">Illustration<", ">Иллюстрация<"),
(">Maps: simulated scenes, illustrations<", ">Карты: симуляции, иллюстрации<"),
("This is how the first product would look: a small compute module that sits on the robot. It is a concept render; no module has been built. What exists today is the design running on an FPGA.",
 "Так мог бы выглядеть первый продукт: небольшой вычислительный модуль на роботе. Это концепт-рендер, модуль ещё не собран. Сегодня есть дизайн, работающий на FPGA."),
(" Form factor<", " Форм-фактор<"),
("One small module. <br>", "Один небольшой модуль. <br>"), (">Plugs into the robot.<", ">Подключается к роботу.<"),
("The first product is an edge module around the chip. Later, the same design as an IP block inside an SoC.",
 "Первый продукт — edge-модуль с чипом. Позже тот же дизайн как IP-блок внутри SoC."),
("Concept render of the Ateno AX module connected to a laptop by a USB-C cable", "Концепт-рендер модуля Ateno AX, подключённого к ноутбуку кабелем USB-C"),
# ---------- team ----------
("From idea to working hardware", "От идеи до работающего железа"), ("in five months.", "за пять месяцев."),
(">Sviatoslav Gladyshev<", ">Святослав Гладышев<"), (">Co-founder &amp; CEO<", ">Сооснователь и CEO<"),
("Mathematics at NYU; condensed-matter research on excitons in bilayer graphene. Previously co-founder and CTO of LevelUp.", "Математика в NYU; исследования экситонов в двухслойном графене. Ранее сооснователь и CTO LevelUp."),
(">Artemii Mavlitov<", ">Артемий Мавлитов<"), (">Co-founder &amp; CTO<", ">Сооснователь и CTO<"),
("Leads RTL design. Data Science and Mathematics at NYU. ICPC and CCPC regional medalist.", "Отвечает за RTL. Data Science и математика в NYU. Призёр региональных этапов ICPC и CCPC."),
# ---------- ask ----------
("Raising a pre-seed round <br>of", "Привлекаем pre-seed <br>на"), (">$1.25M<", ">$1,25 млн<"),
(">GPU benchmark<", ">Бенчмарк против GPU<"), ("Energy per frame, FPGA vs GPU and Jetson, on real scenes.", "Энергия на кадр: FPGA против GPU и Jetson, на реальных сценах."),
(">Large scenes<", ">Большие сцены<"), ("Training and rendering on large, real-world scenes.", "Обучение и рендеринг на больших реальных сценах."),
(">Design partners<", ">Дизайн-партнёры<"), ("First paid engagements with drone and autonomous-system makers.", "Первые платные проекты с производителями дронов и автономных систем."),
# ---------- close ----------
(">Build the map <span", ">Строим карту <span"), (">on the device.</span>", ">прямо на устройстве.</span>"),
("No GPS. No cloud. info@ateno.co · ateno.co", "Без GPS. Без облака. info@ateno.co · ateno.co"),
# ---------- sections / page ----------
('data-section="Problem"', 'data-section="Проблема"'), ('data-section="Product"', 'data-section="Продукт"'), ('data-section="Proof"', 'data-section="Доказательства"'),
('data-section="Business"', 'data-section="Бизнес"'), ('data-section="Team and ask"', 'data-section="Команда и раунд"'),
('<html lang="en">', '<html lang="ru">'), ("<title>Ateno — Pitch Deck</title>", "<title>Ateno — питч-дек</title>"),
("toLocaleString('en-US')", "toLocaleString('ru-RU')"),
]
h = src
missing = []
for a, b in T:
    if a not in h:
        missing.append(a)
    h = h.replace(a, b)
if missing:
    print("NOT FOUND:"); [print("  ", m[:100]) for m in missing]
assert "Elbit" not in h, "Elbit must not appear in the Russian deck"
(out / "index.html").write_text(h, encoding="utf-8")
body = h[h.index("<section"):]
left = sorted(set(t.strip() for t in re.findall(r">([^<>{}]*[A-Za-z]{4,}[^<>{}]*)<", re.sub(r"<svg[\s\S]*?</svg>|<script[\s\S]*?</script>|<style[\s\S]*?</style>", "", body)) if t.strip()))
print("built", out / "index.html", "| english left:", left[:40])
