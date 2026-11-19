# HK1 (Allwinner RBOX H8) — a build do Free My TV para essa box

Esta pasta é a **build e as notas da TV box HK1** do usuário (`192.168.0.5`): o APK que está
instalado nela, o script que o recompila e o que foi preciso mudar no app para ele rodar.

É um **projeto paralelo** ao da TX9 (`tx9/`), não uma continuação dele: as duas boxes são de
fabricantes e Android diferentes, e cada uma tem a sua pasta. O que é comum fica no app (o
repositório), o que é de cada box fica na pasta dela.

## O aparelho

| | |
|---|---|
| Modelo | HK1 RBOX H8 (Allwinner `apollo-p2`, SoC `sun50iw9p1`), Android TV-like, launcher `com.hisight.mslauncher` |
| IP | `192.168.0.5` (Wi-Fi), fuso `America/Recife` → a cidade vem do fuso no build `--generic` |
| Android | **12 (API 31)** |
| ABI | `armeabi-v7a` (32 bits), 4 núcleos |
| Tela | 1920×1080, densidade 240 |
| Memória | **2 GB** (o app a trata como *small memory*: os caminhos de desenho mais baratos, sem as camadas offscreen) |
| Espaço | 11 GB, 1,5 GB livres (87 % usado — apertado para instalar) |
| Root | **não** — `adb shell` roda como `shell` (uid 2000), `ro.adb.secure=1` |
| ADB | `adbd` na 5555, atende **um cliente por vez** |
| Patch | 2022-02-05 (o fingerprint é do `sailfish` do Google, o do fabricante) |

### Sem `leanback`, com telephony

A box **não declara `android.software.leanback`** ✗ e declara `android.hardware.telephony` ✓ — as
duas coisas que fazem o app confundir uma box com um celular ✗.

O que salva é o `com.android.tv.settings` ✓ (as *Android TV settings*, que um celular não tem):
o app procura esse pacote para saber que é uma TV ✓ — a mesma saída que a TX9 usa ✗ (lá sem
`leanback` e com telephony ✓, e o `com.android.tv.settings` presente ✓).

## O APK

| | |
|---|---|
| Arquivo | `FreeMyTV-hk1.apk` (1,7 MB) — a mesma build (mesmo código, mesma chave) que está instalada na box |
| Assinatura | `CN=Free My TV`, SHA-256 `4d395e7728d8554f93055db6de24a909a3eba39fdedbec1669fce90e2aeb516d` |
| Chave | `freemytv.keystore` na raiz do projeto (senha `freemytv`, alias `freemytv`) |
| Build | `./build.sh --generic` (sem `config.properties`: sem chave do TMDB, cidade pelo fuso) |

**Sem `--min-sdk`**: a HK1 roda Android 12 ✓, então vale o piso do projeto (26) ✓. A TX9 ✗ precisa
de `--min-sdk=25` ✗ por causa do Android 7 ✗.

A chave é **local**, não a de release do projeto (`b85d4ff6…`). Consequências: o app **não se
atualiza sozinho** pelas releases do GitHub, e instalar uma release oficial exigiria desinstalar
antes (assinatura diferente). Para atualizar esta box, recompile e reinstale com a **mesma**
`freemytv.keystore`.

`*.apk` e `*.keystore` estão no `.gitignore`: a pasta entra no git só com o texto e as imagens.

## Recompilar

```bash
./hk1/build-hk1.sh              # só compila e copia para hk1/FreeMyTV-hk1.apk
./hk1/build-hk1.sh --install    # compila, instala na box e solta a conexão
```

O script é o do da TX9 (`tx9/build-tx9.sh`) sem a parte do `--min-sdk=25`, e com o IP desta box.
As duas particularidades desta máquina (os caminhos Windows no Git Bash e o JDK 17) estão
resolvidas nele ✓ — veja a `tx9/README.md` para o porquê de cada uma ✓.

## Antes de trocar de modo: solte o computador

O `adbd` dessa box **atende um cliente por vez** ✓. Com o `adb` do PC conectado ✗, o app não
consegue falar com o ADB dela ✗ e a troca falha com *"o ADB da TV não respondeu"* ✗ (é o caso #221
do projeto ✓).

```bash
adb disconnect 192.168.0.5:5555
adb kill-server
```

Depois é só apertar na box: **Free My TV → Início → Free My TV → OK** ✓.

## O que já vem na box

A HK1 já tem **Aurora Store** ✓ (`com.aurora.store`) e **F-Droid** ✓ (`org.fdroid.fdroid`)
instalados ✓ — o Free My TV lista os dois na linha *Loja de aplicativos* ✓, então dá para escolher
qual das duas está em uso ✓ sem instalar nada ✗.

Apps do launcher na box: Chrome ✓, YouTube TV ✓, Play Store ✓, Aurora Store ✓, F-Droid ✓, VLC ✓,
KMPlayer ✓, Xplore ✓, SuperSU ✓ (mas a box **não tem root** ✓), o gerenciador de arquivos da
Softwinner ✓, o Fire Player ✓ e o espelhamento ✓.

## O que o app liga e desliga nela

A HK1 é uma ROM da **Allwinner** ✓ (a Softwinner é a marca dela ✓), então os apps de fábrica são
outros ✗ — e o app precisou de listas próprias ✗ (as da TX9 ✗ são de outra ROM ✗).

**Desligados** ✗ (o `DEBLOAT` ✗, apps de fábrica que só atrapalham ✓):

| App | O que é |
|---|---|
| `com.softwinner.fireplayer` | o player de vídeo |
| `com.softwinner.miracastReceiver` | o espelhamento de tela |
| `com.softwinner.TvdFileManager` | o gerenciador de arquivos |
| `com.rockchip.devicetest` | teste de fábrica |
| `com.system.dota` | os "dragon box" de teste |

**Nunca desligados** ✗ (o `PROTECTED` ✗, peças do sistema ✓):

| App | O que é |
|---|---|
| `com.softwinner.update` | a atualização da ROM |
| `com.softwinner.awmanager` | o gerenciador de apps do sistema |
| `com.softwinner.provision` | a preparação da ROM |
| `com.allwinnertech.packageoverride` | a instalação de pacotes |
| `com.hisight.mslauncher` | o launcher da box (é o "Início original" ✗) |
| `tv.autostart` | o que abre o launcher no boot ✗ |
| `com.softwinner.theme.icon`, `com.softwinner.theme.color` | os temas |
| `com.softwinner.timerswitch` | o desligamento automático |

## O que já foi testado

- [x] O app instala ✓ e abre ✓ (a box não tem root ✗, mas não precisa ✗).
- [x] O app **reconhece a box como TV** ✓ — sem `leanback` ✗ e com telephony ✓, quem decide é o
      `com.android.tv.settings` ✓, presente ✓.
- [x] A troca de modo ✓: o app fala com o ADB dela própria ✓, e o `Início` passa a ser o
      `io.freemytv/.HomeActivity` ✓ (o launcher `com.hisight.mslauncher` é desligado ✓).
- [x] A tela inicial sobe ✓, com o desenho mais barato ✓ (2 GB de RAM ✓ → `Ui.LEGACY` ✓).

## O que ainda falta testar

- [ ] A tela de descanso (o `com.android.dreams.web` é o da ROM ✗; o app traz o dele ✓).
- [ ] O *Ao ligar → Início* (a box precisa de uma rede que conecte depois da tela ✓, como na TX9 ✓).
- [ ] Com 2 GB de RAM ✓ o app usa os caminhos de desenho baratos ✓ — dá para ver se a animação fica
      lisa ✓.
- [ ] A loja de aplicativos ✓ (a box tem as duas ✓ — Aurora Store ✓ e F-Droid ✓ — para escolher ✓).
