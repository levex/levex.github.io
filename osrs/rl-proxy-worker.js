const TARGET = 'https://repo.runelite.net/net/runelite/client/maven-metadata.xml';

export default {
  async fetch(request) {
    const origin = request.headers.get('Origin') ?? '*';

    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: cors(origin),
      });
    }

    const res = await fetch(TARGET, {
      cf: { cacheTtl: 60, cacheEverything: true },
    });

    const body = await res.text();

    return new Response(body, {
      status: res.status,
      headers: {
        'Content-Type': 'application/xml',
        ...cors(origin),
      },
    });
  },
};

function cors(origin) {
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Max-Age': '86400',
  };
}
