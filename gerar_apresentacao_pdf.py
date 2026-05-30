from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit


PDF_PATH = "/workspace/APRESENTACAO_PRONTA_KEVIN_MAIKON.pdf"
W, H = 960, 540

NAVY = colors.HexColor("#0B2D52")
DARK = colors.HexColor("#071C33")
BLUE = colors.HexColor("#12385F")
GREEN = colors.HexColor("#20B96F")
LIGHT_GREEN = colors.HexColor("#DFF5EA")
RED = colors.HexColor("#E95656")
YELLOW = colors.HexColor("#F2B84B")
BG = colors.HexColor("#F7FBFF")
TEXT = colors.HexColor("#263D55")
MUTED = colors.HexColor("#536B84")
LINE = colors.HexColor("#D7E2EE")
WHITE = colors.white


def wrap_text(text, font_name, font_size, max_width):
    lines = []
    for part in str(text).split("\n"):
        if not part:
            lines.append("")
            continue
        lines.extend(simpleSplit(part, font_name, font_size, max_width))
    return lines


def draw_background(c, slide_no, label):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#E9F4FF"))
    c.circle(835, 465, 155, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#E7F8EF"))
    c.circle(95, 50, 135, stroke=0, fill=1)
    c.setStrokeColor(colors.HexColor("#DCE8F3"))
    c.setLineWidth(0.7)
    for x in range(0, W, 48):
        c.line(x, 0, x, H)
    for y in range(0, H, 48):
        c.line(0, y, W, y)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(46, 22, label)
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - 46, 22, f"{slide_no:02d}")


def draw_title(c, title, tag, subtitle=None):
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(W - 46, H - 48, tag.upper())
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 26)
    y = H - 58
    for line in wrap_text(title, "Helvetica-Bold", 26, 710):
        c.drawString(46, y, line)
        y -= 30
    if subtitle:
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 13)
        y -= 5
        for line in wrap_text(subtitle, "Helvetica", 13, 780):
            c.drawString(46, y, line)
            y -= 18
    return y - 10


def card(c, x, y, w, h, title, body=None, accent=GREEN, dark=False):
    c.setFillColor(DARK if dark else WHITE)
    c.setStrokeColor(DARK if dark else LINE)
    c.roundRect(x, y, w, h, 14, stroke=1, fill=1)
    c.setFillColor(accent)
    c.roundRect(x, y, 8, h, 4, stroke=0, fill=1)
    c.setFillColor(WHITE if dark else BLUE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x + 20, y + h - 25, title)
    if body:
        c.setFillColor(colors.HexColor("#DCEBFA") if dark else TEXT)
        c.setFont("Helvetica", 10.5)
        ty = y + h - 46
        for line in wrap_text(body, "Helvetica", 10.5, w - 35):
            c.drawString(x + 20, ty, line)
            ty -= 14


def bullets(c, items, x, y, max_width, font_size=11, color=TEXT, bullet_color=GREEN, leading=15):
    c.setFont("Helvetica", font_size)
    c.setFillColor(color)
    for item in items:
        lines = wrap_text(item, "Helvetica", font_size, max_width - 18)
        c.setFillColor(bullet_color)
        c.circle(x + 4, y - 3, 2.4, stroke=0, fill=1)
        c.setFillColor(color)
        for i, line in enumerate(lines):
            c.drawString(x + 14, y, line)
            if i < len(lines) - 1:
                y -= leading
        y -= leading + 2
    return y


def draw_table(c, x, y, col_widths, row_h, headers, rows, font_size=9.4):
    total_w = sum(col_widths)
    c.setFillColor(NAVY)
    c.roundRect(x, y - row_h, total_w, row_h, 9, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", font_size)
    cx = x
    for i, htxt in enumerate(headers):
        c.drawString(cx + 8, y - 17, htxt)
        cx += col_widths[i]
    y -= row_h
    c.setFont("Helvetica", font_size)
    for r, row in enumerate(rows):
        fill = WHITE if r % 2 == 0 else colors.HexColor("#F2F7FC")
        c.setFillColor(fill)
        c.rect(x, y - row_h, total_w, row_h, stroke=0, fill=1)
        c.setStrokeColor(LINE)
        c.line(x, y - row_h, x + total_w, y - row_h)
        cx = x
        c.setFillColor(TEXT)
        for i, txt in enumerate(row):
            lines = wrap_text(txt, "Helvetica", font_size, col_widths[i] - 14)
            ty = y - 15
            for line in lines[:3]:
                c.drawString(cx + 8, ty, line)
                ty -= font_size + 2
            cx += col_widths[i]
        y -= row_h


def tools_grid(c):
    tools = [
        ("P", "Prometheus", "Coleta e armazena métricas em séries temporais."),
        ("G", "Grafana", "Cria dashboards executivos e técnicos."),
        ("A", "Alertmanager", "Envia alertas automáticos e escalonados."),
        ("J", "JMeter", "Executa testes estruturados de carga."),
        ("L", "Locust", "Simula usuários com cenários em Python."),
    ]
    x, y, w, h, gap = 46, 235, 160, 145, 17
    for i, (letter, name, desc) in enumerate(tools):
        xx = x + i * (w + gap)
        c.setFillColor(WHITE)
        c.setStrokeColor(LINE)
        c.roundRect(xx, y, w, h, 14, stroke=1, fill=1)
        c.setFillColor(NAVY)
        c.circle(xx + w / 2, y + h - 42, 21, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 17)
        c.drawCentredString(xx + w / 2, y + h - 48, letter)
        c.setFillColor(BLUE)
        c.setFont("Helvetica-Bold", 12.5)
        c.drawCentredString(xx + w / 2, y + 62, name)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 9.3)
        ty = y + 43
        for line in wrap_text(desc, "Helvetica", 9.3, w - 22):
            c.drawCentredString(xx + w / 2, ty, line)
            ty -= 12


def new_slide(c, number, title, tag, subtitle=None, label="E-Fecaf Global"):
    draw_background(c, number, label)
    return draw_title(c, title, tag, subtitle)


def generate():
    c = canvas.Canvas(PDF_PATH, pagesize=(W, H))
    c.setTitle("Monitoramento Continuo de Performance - E-Fecaf Global")
    c.setAuthor("Kevin Maikon Caetano de Andrade Santos")

    # Slide 1
    c.setFillColor(DARK)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#12385F"))
    c.circle(815, 430, 170, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#0F6B47"))
    c.circle(120, 70, 120, stroke=0, fill=1)
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(58, 480, "QUALITY ASSURANCE | UNIFECAF")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 38)
    c.drawString(58, 392, "Monitoramento Contínuo")
    c.drawString(58, 350, "de Performance")
    c.setFont("Helvetica", 18)
    c.setFillColor(colors.HexColor("#D8EBFF"))
    c.drawString(58, 306, "Solução para e-commerce com Prometheus, Grafana,")
    c.drawString(58, 282, "Alertmanager, JMeter e Locust")
    card(c, 58, 70, 560, 125, "Identificação", "Aluno: Kevin Maikon Caetano de Andrade Santos\nUniversidade: UniFECAF\nDisciplina: Quality Assurance\nData: 30 de maio de 2026", accent=GREEN, dark=True)
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - 46, 22, "01")
    c.showPage()

    # Slide 2
    new_slide(c, 2, "Introdução: contexto do desafio", "Problema", "A E-Fecaf Global é um e-commerce em expansão que sofre com lentidão, quedas e perda de vendas em picos de acesso.", "Introdução")
    card(c, 54, 120, 405, 260, "Impactos identificados", accent=RED)
    bullets(c, ["Lentidão em páginas e checkout.", "Quedas durante campanhas promocionais.", "Abandono de carrinho e perda de receita.", "Reclamações em canais digitais.", "Dificuldade para encontrar a causa raiz."], 78, 335, 340, 12)
    card(c, 500, 120, 405, 260, "Objetivo da solução", accent=GREEN)
    bullets(c, ["Implantar monitoramento contínuo.", "Visualizar indicadores em tempo real.", "Configurar alertas automáticos.", "Executar testes de estresse.", "Otimizar a plataforma com base em dados."], 524, 335, 340, 12)
    c.showPage()

    # Slide 3
    new_slide(c, 3, "Principais desafios", "Diagnóstico", "Os desafios se conectam: sem visibilidade e alertas, a equipe responde tarde e o impacto no negócio aumenta.", "Desafios")
    cards = [
        ("Lentidão", ["Páginas lentas.", "Checkout com atrasos.", "APIs degradadas em pico."], RED),
        ("Indisponibilidade", ["Quedas em promoções.", "Compra interrompida.", "Perda de confiança."], RED),
        ("Falta de visibilidade", ["Métricas descentralizadas.", "Gargalos ocultos.", "Baixa correlação de falhas."], YELLOW),
        ("Falta de alertas", ["Incidentes descobertos tarde.", "Recuperação lenta.", "Risco em datas críticas."], YELLOW),
    ]
    x = 46
    for title, items, accent in cards:
        card(c, x, 172, 205, 210, title, accent=accent)
        bullets(c, items, x + 20, 326, 165, 10.8, leading=14)
        x += 222
    c.showPage()

    # Slide 4
    new_slide(c, 4, "Arquitetura de monitoramento contínuo", "Solução proposta", "A proposta combina coleta, dashboards, alertas e testes para criar um ciclo de melhoria permanente.", "Arquitetura")
    boxes = [("Aplicações, APIs,\nservidores e banco\nexpõem métricas", 58), ("Prometheus coleta\ne armazena séries\ntemporais", 360), ("Grafana visualiza\ne Alertmanager\nnotifica equipes", 662)]
    for txt, x in boxes:
        card(c, x, 245, 240, 110, "", txt, accent=GREEN)
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 32)
    c.drawString(315, 288, "→")
    c.drawString(617, 288, "→")
    card(c, 170, 118, 620, 72, "JMeter e Locust", "Geram carga controlada para validar a capacidade em cenários como Black Friday.", accent=YELLOW)
    c.showPage()

    # Slide 5
    new_slide(c, 5, "Ferramentas propostas", "Ferramentas", "Cada ferramenta possui uma função específica na solução de observabilidade e testes.", "Ferramentas")
    tools_grid(c)
    card(c, 110, 110, 740, 70, "Resultado esperado", "Maior previsibilidade, identificação rápida de gargalos, redução de incidentes e melhoria da experiência do cliente.", accent=GREEN)
    c.showPage()

    # Slide 6
    new_slide(c, 6, "Prometheus", "Coleta de métricas", "Núcleo da solução para coletar e consultar métricas técnicas e de negócio em tempo real.", "Prometheus")
    card(c, 58, 128, 390, 265, "Como funciona", accent=GREEN)
    bullets(c, ["Modelo pull para coleta de métricas.", "Consulta endpoints HTTP de aplicações e exporters.", "Armazena dados como séries temporais.", "Permite análise com PromQL.", "Integra-se ao Alertmanager."], 82, 348, 325, 12)
    card(c, 510, 128, 390, 265, "Benefícios", accent=GREEN)
    bullets(c, ["Monitoramento em tempo real.", "Flexibilidade para métricas técnicas e de negócio.", "Identificação rápida de anomalias.", "Base sólida para melhoria contínua.", "Exemplo: http_request_duration_seconds."], 534, 348, 325, 12)
    c.showPage()

    # Slide 7
    new_slide(c, 7, "Grafana: dashboards em tempo real", "Visualização", "Transforma métricas em painéis claros para equipes técnicas, gestores e áreas de negócio.", "Grafana")
    metrics = [("Disponibilidade", "99,4%", GREEN), ("Resposta média", "1,6s", GREEN), ("Erros 5xx", "2,1%", YELLOW), ("Requisições/min", "42k", GREEN), ("CPU média", "71%", YELLOW), ("Alertas ativos", "3", RED)]
    x0, y0 = 70, 292
    for i, (name, val, color) in enumerate(metrics):
        x = x0 + (i % 3) * 275
        y = y0 - (i // 3) * 120
        card(c, x, y, 230, 82, name, accent=color, dark=True)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(x + 22, y + 24, val)
    c.showPage()

    # Slide 8
    new_slide(c, 8, "Alertmanager", "Alertas automáticos", "Recebe alertas do Prometheus, organiza notificações e reduz o tempo de resposta a incidentes.", "Alertmanager")
    card(c, 58, 150, 380, 230, "Canais de notificação", accent=GREEN)
    bullets(c, ["E-mail corporativo.", "Microsoft Teams, Slack ou Google Chat.", "Sistemas de chamados.", "Ferramentas de plantão.", "Escalonamento para DevOps e liderança."], 82, 335, 320, 12)
    card(c, 510, 150, 380, 230, "Fluxo de resposta", accent=YELLOW)
    bullets(c, ["Prometheus detecta condição crítica.", "Alertmanager agrupa e classifica.", "Equipe recebe alerta acionável.", "Responsáveis executam correção.", "Incidentes graves são escalonados."], 534, 335, 320, 12)
    c.showPage()

    # Slide 9
    new_slide(c, 9, "Métricas essenciais monitoradas", "Métricas", "As métricas foram escolhidas por relação direta com performance, disponibilidade e experiência do cliente.", "Métricas")
    draw_table(c, 55, 380, [170, 310, 360], 45, ["Métrica", "Objetivo", "Exemplo de uso"], [
        ["Tempo de resposta", "Medir velocidade percebida pelo usuário.", "Checkout deve responder em até 2 segundos."],
        ["Latência", "Avaliar atraso em APIs e integrações.", "Identificar APIs lentas em horários de pico."],
        ["Disponibilidade", "Controlar estabilidade do e-commerce.", "Manter disponibilidade acima de 99%."],
        ["CPU e memória", "Medir carga e consumo dos serviços.", "Prever escala ou investigar vazamentos."],
        ["Taxa de erros", "Medir falhas em requisições.", "Alertar quando erros superarem 5%."],
    ])
    c.showPage()

    # Slide 10
    new_slide(c, 10, "Configuração de alertas", "Alertas", "Bons alertas indicam o que está acontecendo, onde está o problema e qual é a severidade.", "Configuração")
    draw_table(c, 55, 390, [330, 140, 370], 46, ["Condição", "Severidade", "Ação recomendada"], [
        ["CPU acima de 85% por 5 minutos", "Alta", "Verificar saturação e escalar servidores."],
        ["Memória acima de 90% por 5 minutos", "Alta", "Investigar vazamento ou aumentar recursos."],
        ["Tempo de resposta acima de 2 segundos", "Crítica", "Avaliar APIs, banco de dados e cache."],
        ["Disponibilidade abaixo de 99%", "Crítica", "Acionar plano de incidente."],
        ["Taxa de erro acima de 5%", "Crítica", "Identificar serviço com falha e corrigir."],
    ])
    c.showPage()

    # Slide 11
    new_slide(c, 11, "Exemplo de regra Prometheus", "PromQL", "A regra abaixo demonstra um alerta de alto uso de CPU encaminhado ao Alertmanager.", "Regra de alerta")
    c.setFillColor(DARK)
    c.roundRect(60, 145, 500, 250, 14, stroke=0, fill=1)
    code = [
        "groups:",
        "  - name: e-fecaf-alertas",
        "    rules:",
        "      - alert: AltoUsoCPU",
        '        expr: avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) * 100 > 85',
        "        for: 5m",
        "        labels:",
        "          severity: alta",
        "        annotations:",
        '          summary: \"Uso de CPU acima de 85%\"',
    ]
    c.setFillColor(colors.HexColor("#DFF5EA"))
    c.setFont("Courier", 8.7)
    y = 370
    for line in code:
        c.drawString(78, y, line)
        y -= 19
    card(c, 600, 145, 300, 250, "Como isso ajuda", accent=GREEN)
    bullets(c, ["Detecção automática de risco.", "Alerta só dispara após 5 minutos.", "Reduz ruído operacional.", "Notificação chega aos responsáveis.", "Permite ação antes do impacto ao cliente."], 624, 348, 240, 11.5)
    c.showPage()

    # Slide 12
    new_slide(c, 12, "Testes de estresse com JMeter", "JMeter", "Ferramenta para testes de carga, estresse e performance em aplicações web, APIs e serviços.", "JMeter")
    steps = [("1", "Cenários", "Home, busca, produto, carrinho, checkout e pagamento."), ("2", "Usuários", "Configurar usuários virtuais simultâneos."), ("3", "Ramp-up", "Definir crescimento gradual de carga."), ("4", "Execução", "Rodar em ambiente controlado."), ("5", "Análise", "Avaliar resposta, throughput e erros.")]
    x = 48
    for n, title, desc in steps:
        card(c, x, 198, 160, 160, title, desc, accent=GREEN)
        c.setFillColor(GREEN)
        c.circle(x + 28, 326, 16, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(x + 28, 321, n)
        x += 176
    c.showPage()

    # Slide 13
    new_slide(c, 13, "Testes de estresse com Locust", "Locust", "Complementa o JMeter com cenários programáveis em Python e execução distribuída.", "Locust")
    card(c, 58, 140, 380, 250, "Vantagens", accent=GREEN)
    bullets(c, ["Cenários escritos em Python.", "Comportamento real de usuários.", "Execução distribuída para altos volumes.", "Interface web em tempo real.", "Boa integração com pipelines DevOps."], 82, 346, 315, 12)
    draw_table(c, 492, 360, [120, 150, 170], 42, ["Critério", "JMeter", "Locust"], [
        ["Abordagem", "Planos visuais", "Código Python"],
        ["Facilidade", "Boa inicial", "Boa com Python"],
        ["Escalabilidade", "Boa", "Muito boa"],
        ["Cenários", "Visual", "Mais flexível"],
    ], font_size=8.8)
    c.showPage()

    # Slide 14
    new_slide(c, 14, "Simulação de Black Friday", "Cenário de teste", "A carga cresce progressivamente para validar estabilidade, checkout, APIs, banco de dados e autoscaling.", "Black Friday")
    c.setStrokeColor(NAVY)
    c.setLineWidth(2.5)
    c.line(95, 150, 95, 365)
    c.line(95, 150, 550, 150)
    points = [(150, 190, "1.000"), (270, 235, "5.000"), (390, 285, "10.000"), (510, 345, "20.000")]
    c.setStrokeColor(GREEN)
    c.setLineWidth(4)
    for (x1, y1, _), (x2, y2, _) in zip(points, points[1:]):
        c.line(x1, y1, x2, y2)
    for x, y, label in points:
        c.setFillColor(GREEN)
        c.circle(x, y, 8, stroke=0, fill=1)
        c.setFillColor(TEXT)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(x, 125, label + " usuários")
    card(c, 610, 138, 300, 245, "Resultados esperados", accent=GREEN)
    bullets(c, ["Disponibilidade acima de 99%.", "Tempo médio abaixo de 2 segundos.", "Taxa de erro abaixo de 5%.", "Checkout funcional durante todo o teste.", "Gargalos identificados com evidência."], 634, 342, 240, 11.5)
    c.showPage()

    # Slide 15
    new_slide(c, 15, "Gargalos plausíveis encontrados", "Análise", "Monitoramento e testes permitem apontar gargalos com base em dados, não em suposições.", "Gargalos")
    cards = [
        ("Banco de dados", ["Consultas sem índice.", "Busca lenta.", "Bloqueios em pedidos."], RED),
        ("Servidores", ["CPU acima de 85%.", "Memória acima de 90%.", "Escala insuficiente."], RED),
        ("APIs", ["Checkout acima de 2s.", "Erros 500 em pagamento.", "Conexões limitadas."], YELLOW),
        ("Rede", ["Serviços externos lentos.", "Ausência de CDN.", "Gargalo no balanceador."], YELLOW),
    ]
    x = 46
    for title, items, accent in cards:
        card(c, x, 172, 205, 210, title, accent=accent)
        bullets(c, items, x + 20, 326, 165, 10.8, leading=14)
        x += 222
    c.showPage()

    # Slide 16
    new_slide(c, 16, "Propostas de otimização", "Melhoria contínua", "As ações devem ser priorizadas por impacto no checkout, pagamento, disponibilidade e receita.", "Otimizações")
    opts = [
        ("Balanceamento", "Distribuir requisições e evitar sobrecarga em uma instância."),
        ("Cache", "Reduzir consultas repetidas e acelerar páginas e produtos."),
        ("SQL otimizado", "Criar índices, revisar queries lentas e reduzir bloqueios."),
        ("Escala horizontal", "Adicionar instâncias automaticamente em picos."),
        ("CDN", "Entregar imagens e arquivos estáticos com menor latência."),
        ("Revisão contínua", "Ajustar SLAs, alertas e capacidade com base no histórico."),
    ]
    for i, (title, desc) in enumerate(opts):
        x = 58 + (i % 3) * 295
        y = 270 - (i // 3) * 120
        card(c, x, y, 250, 90, title, desc, accent=GREEN)
    c.showPage()

    # Slide 17
    new_slide(c, 17, "Benefícios esperados", "Resultados", "A empresa passa de uma operação reativa para uma operação preventiva, orientada por dados.", "Benefícios")
    benefits = [("Disponibilidade", "+99%", "Meta de estabilidade."), ("Resposta", "<2s", "Meta para checkout."), ("Erros", "<5%", "Controle de falhas."), ("Recuperação", "MTTR", "Resposta mais rápida.")]
    x = 58
    for title, val, desc in benefits:
        card(c, x, 278, 190, 105, title, accent=GREEN, dark=True)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 23)
        c.drawString(x + 22, 318, val)
        c.setFont("Helvetica", 10)
        c.drawString(x + 22, 298, desc)
        x += 218
    card(c, 105, 145, 345, 85, "Valor para o cliente", "Site mais rápido, checkout confiável e menos frustração em promoções.", accent=GREEN)
    card(c, 510, 145, 345, 85, "Valor para o negócio", "Menor abandono de carrinho, aumento de vendas e confiança na marca.", accent=GREEN)
    c.showPage()

    # Slide 18
    new_slide(c, 18, "Conclusão e referências", "Encerramento", "A solução integra monitoramento, visualização, alertas e testes para garantir estabilidade em picos de tráfego.", "Conclusão")
    card(c, 58, 287, 390, 112, "Resumo da solução", "Prometheus coleta métricas; Grafana exibe dashboards; Alertmanager notifica equipes; JMeter e Locust validam capacidade.", accent=GREEN)
    card(c, 510, 287, 390, 112, "Conclusão", "Monitoramento contínuo é um processo permanente de prevenção de falhas, melhoria da experiência e proteção da receita.", accent=GREEN)
    refs = [
        "Apache JMeter User Manual - https://jmeter.apache.org/usermanual/",
        "Grafana Documentation - https://grafana.com/docs/grafana/latest/",
        "Locust Documentation - https://docs.locust.io/",
        "Prometheus Documentation - https://prometheus.io/docs/",
        "Alertmanager Documentation - https://prometheus.io/docs/alerting/latest/alertmanager/",
        "GOOGLE. Site Reliability Engineering. O'Reilly Media, 2016.",
    ]
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(58, 235, "Referências bibliográficas")
    bullets(c, refs, 58, 212, 810, 9.3, color=TEXT, bullet_color=GREEN, leading=12)
    c.showPage()

    c.save()
    print(PDF_PATH)


if __name__ == "__main__":
    generate()
