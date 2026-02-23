const dgram = require("dgram");

const server = dgram.createSocket("udp4");

server.bind(3004, () => {
  console.log("Servidor UDP escutando na porta 3004");
});
