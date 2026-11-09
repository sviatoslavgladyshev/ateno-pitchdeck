// Small MQTT-over-WebSocket link for the laser pointer. The laser sends many small position updates,
// which the command relay is too slow for. Only coordinates travel here, on the private channel.
(() => {
  const BROKERS = ['wss://broker.hivemq.com:8884/mqtt', 'wss://broker.emqx.io:8084/mqtt'];
  const enc = new TextEncoder(), dec = new TextDecoder();
  const str = s => { const b = enc.encode(s); return [b.length >> 8, b.length & 255, ...b]; };
  const size = n => { const o = []; do { let d = n % 128; n = Math.floor(n / 128); if (n) d |= 128; o.push(d); } while (n); return o; };
  const packet = (type, body) => new Uint8Array([type, ...size(body.length), ...body]);

  function open(url, topic, listen, onOpen, onClose) {
    const ws = new WebSocket(url, 'mqtt');
    ws.binaryType = 'arraybuffer';
    let ping;
    ws.onopen = () => {
      const id = 'ateno' + Math.random().toString(36).slice(2, 12);
      ws.send(packet(0x10, [...str('MQTT'), 4, 2, 0, 60, ...str(id)]));
    };
    ws.onmessage = e => {
      const d = new Uint8Array(e.data);
      for (let i = 0; i < d.length;) {
        const type = d[i] >> 4; let j = i + 1, len = 0, m = 1, b;
        do { b = d[j++]; len += (b & 127) * m; m *= 128; } while (b & 128);
        if (type === 2) {                                // connected
          if (d[j + 1] !== 0) { ws.close(); return; }
          if (listen) ws.send(packet(0x82, [0, 1, ...str(topic), 0]));
          ping = setInterval(() => ws.readyState === 1 && ws.send(new Uint8Array([0xC0, 0])), 30000);
          onOpen(ws);
        } else if (type === 3 && listen) {               // message
          const n = (d[j] << 8) | d[j + 1];
          listen(dec.decode(d.subarray(j + 2 + n, j + len)));
        }
        i = j + len;
      }
    };
    ws.onclose = () => { clearInterval(ping); onClose(); };
    ws.onerror = () => {};
    return ws;
  }

  // Listener: stays on every broker, so it hears a sender on whichever one that sender could reach.
  window.laserListen = (topic, onMessage) => {
    let stopped = false; const socks = new Map();
    const start = url => {
      if (stopped) return;
      socks.set(url, open(url, topic, onMessage, () => {}, () => setTimeout(() => start(url), 4000)));
    };
    BROKERS.forEach(start);
    return { close() { stopped = true; socks.forEach(s => s.close()); } };
  };

  // Sender: uses the first broker it can reach, moving to the next if that one drops.
  window.laserSend = (topic, onState) => {
    let ws = null, i = 0, stopped = false, fails = 0;
    const next = () => {
      if (stopped) return;
      const url = BROKERS[i++ % BROKERS.length];
      let opened = false;
      open(url, topic, null, s => { opened = true; ws = s; fails = 0; onState(true); }, () => {
        ws = null;
        if (opened || ++fails >= BROKERS.length) onState(false);
        setTimeout(next, fails >= BROKERS.length ? 4000 : 300);
      });
    };
    next();
    return {
      send(text) { if (ws?.readyState === 1) ws.send(packet(0x30, [...str(topic), ...enc.encode(text)])); },
      close() { stopped = true; ws?.close(); }
    };
  };
})();
