# Conectar Hostinger a Claude Code

Este repo trae un `.mcp.json` que levanta los servidores MCP de Hostinger
(`hostinger-api-mcp`). Con eso Claude puede leer y operar la VPS, el DNS y
los dominios de la cuenta sin que le pases nada por chat.

Falta un solo paso manual: **el token**. Sin él los servidores arrancan pero
toda llamada devuelve 401.

## 1. Sacar el token

En [hPanel](https://hpanel.hostinger.com/) → menú de la cuenta (arriba a la
derecha) → **API** → *Generar token*. El link directo suele ser
<https://hpanel.hostinger.com/profile/api>.

El token se muestra **una sola vez**. Copialo en ese momento.

Tiene alcance de cuenta entera: quien lo tenga puede reinstalar la VPS,
cambiar DNS y comprar dominios. Tratalo como una contraseña — no va en el
repo, no va pegado en un chat, y si se filtró se revoca desde la misma
pantalla.

## 2. Cargar el token

El `.mcp.json` no guarda el token: guarda `${HOSTINGER_API_TOKEN}`, que
Claude Code expande desde el entorno. Dónde definir esa variable depende de
dónde corras Claude.

### Claude Code en la web (sesiones en la nube)

Las sesiones de [claude.ai/code](https://claude.ai/code) corren en un
contenedor efímero de Linux, sin navegador. Ahí el token es obligatorio: el
login por OAuth del paquete abre una ventana del navegador y en un
contenedor headless no hay forma de completarlo.

Se carga una vez en la configuración del *environment*: **Settings →
Environments → (el environment del repo) → Environment variables**, con
nombre `HOSTINGER_API_TOKEN`. Queda guardado del lado de Anthropic y se
inyecta en cada sesión nueva.

Ojo: con el token cargado los servidores levantan, pero hoy las llamadas no
salen igual — ver *Limitación: las sesiones web no llegan a la API* más abajo.

### Claude Code local (Windows)

Definí la variable de usuario una vez en PowerShell y reiniciá la terminal:

```powershell
setx HOSTINGER_API_TOKEN "el-token-que-copiaste"
```

**Ojo con `npx` en Windows.** El `.mcp.json` del repo usa `npx` a secas
porque es lo que funciona en Linux y macOS. Si en tu máquina los servidores
quedan en *failed*, es porque Windows necesita `npx.cmd`. No edites el
archivo versionado — Claude Code lee también `.mcp.local.json` (no
versionado), así que copiá el `.mcp.json`, cambiá los seis `"command":
"npx"` por `"npx.cmd"` y guardalo como `.mcp.local.json`.

## 3. Verificar

Abrí una sesión nueva (los servidores MCP se leen al arrancar, no en
caliente). Claude va a pedir aprobación para los servidores del repo la
primera vez. Después:

```
/mcp
```

Los seis tienen que figurar como *connected*. Para probar que el token sirve,
pedile a Claude que liste las VPS: usa `VPS_getVirtualMachinesV1` y tiene que
devolver la máquina, no un 401.

## Qué queda disponible

| Servidor | Tools | Para qué |
| --- | --- | --- |
| `hostinger-vps` | 62 | Encender/apagar, snapshots, backups, firewall, claves SSH, proyectos Docker Compose, métricas |
| `hostinger-dns` | 8 | Zonas y registros |
| `hostinger-domains` | 40 | Dominios, nameservers, WHOIS |
| `hostinger-hosting` | 56 | Hosting compartido |
| `hostinger-billing` | 9 | Suscripciones y facturación |
| `hostinger-reach` | 45 | Email marketing |

Son 220 tools en total. Si querés achicar eso, borrá del `.mcp.json` los
bloques que no uses — para lo que hace este repo alcanzan `hostinger-vps`,
`hostinger-dns` y `hostinger-domains`.

## Limitación: las sesiones web no llegan a la API

**Comprobado el 21/08/2026 y sin resolver.** El proxy de egress de Claude Code
en la web bloquea `developers.hostinger.com`, que es el host contra el que
pegan todos estos servidores:

```
curl https://developers.hostinger.com/api/vps/v1/virtual-machines
curl: (56) CONNECT tunnel failed, response 403
```

El 403 aparece al abrir el túnel, antes de mandar el request — o sea que es
política de red por host, no un problema de token ni de permisos de la API.
Que `npx` baje paquetes de npm sin drama en la misma sesión confirma que el
proxy en sí funciona: lo que no está en la lista blanca es Hostinger.

Consecuencia práctica: **el `.mcp.json` sirve en Claude Code local, no en las
sesiones de claude.ai/code.** Los servidores levantan igual en la web, pero
toda llamada muere en el proxy.

Para habilitarlo hay que tocar la política de red del *environment* (se elige
al crearlo) y sumar `developers.hostinger.com` a los hosts permitidos. Está
documentado en
<https://code.claude.com/docs/en/claude-code-on-the-web>.

## Detalle importante: la API no da shell

Estos servidores hablan con la API de Hostinger, no con la VPS por SSH. Sirven
para administrar la máquina desde afuera (estado, red, firewall, snapshots,
desplegar un `docker-compose.yml`), pero no para correr comandos sueltos
adentro. Para eso hace falta SSH aparte.

## La versión está clavada

`hostinger-api-mcp@1.45.5`, no `@latest`. Con `@latest`, `npx` consulta el
registro en cada arranque de sesión — seis veces, una por servidor. Clavada,
usa la copia en caché y levanta en ~3 segundos. Para actualizar: cambiá el
número en los seis lugares del `.mcp.json`.
