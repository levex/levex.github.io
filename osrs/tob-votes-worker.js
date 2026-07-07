// Bindings required in wrangler.toml:
//   [[kv_namespaces]]
//   binding = "VOTES_KV"
//   id = "<your-kv-namespace-id>"
//
// Routes: deploy to tob-votes.<your-subdomain>.workers.dev
//         or bind to a custom route like xarp.us/api/tob-votes

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Max-Age': '86400',
};

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }

    const url = new URL(request.url);

    if (url.pathname === '/votes') {
      if (request.method === 'GET') return handleGet(env);
      if (request.method === 'POST') return handlePost(request, env);
    }

    if (url.pathname === '/voters' && request.method === 'GET') {
      return handleGetVoters(env);
    }

    return new Response('Not found', { status: 404, headers: CORS });
  },
};

async function handleGet(env) {
  const votes = (await env.VOTES_KV.get('votes', 'json')) ?? {};
  return json(votes);
}

async function handleGetVoters(env) {
  const voters = (await env.VOTES_KV.get('voters', 'json')) ?? {};
  return json(voters);
}

async function handlePost(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    return new Response('Bad request', { status: 400, headers: CORS });
  }

  const { itemId, vote, voterId, name } = body;
  if (!itemId || !voterId || !['major', 'minor'].includes(vote)) {
    return new Response('Invalid payload', { status: 400, headers: CORS });
  }

  const voterKey = `voter:${voterId}:${itemId}`;
  const [votes, voters, previousVote] = await Promise.all([
    env.VOTES_KV.get('votes', 'json').then(v => v ?? {}),
    env.VOTES_KV.get('voters', 'json').then(v => v ?? {}),
    env.VOTES_KV.get(voterKey),
  ]);

  if (!votes[itemId]) votes[itemId] = { major: 0, minor: 0 };

  if (previousVote) {
    votes[itemId][previousVote] = Math.max(0, votes[itemId][previousVote] - 1);
  }

  // Update voter record
  if (!voters[voterId]) voters[voterId] = { name: name || voterId, votes: {} };
  if (name) voters[voterId].name = name;

  if (vote !== previousVote) {
    votes[itemId][vote]++;
    voters[voterId].votes[itemId] = vote;
    await env.VOTES_KV.put(voterKey, vote, { expirationTtl: 60 * 60 * 24 * 180 });
  } else {
    // Same vote again = toggle off
    delete voters[voterId].votes[itemId];
    await env.VOTES_KV.delete(voterKey);
  }

  await Promise.all([
    env.VOTES_KV.put('votes', JSON.stringify(votes)),
    env.VOTES_KV.put('voters', JSON.stringify(voters)),
  ]);

  return json(votes);
}

function json(data) {
  return new Response(JSON.stringify(data), {
    headers: { ...CORS, 'Content-Type': 'application/json' },
  });
}
