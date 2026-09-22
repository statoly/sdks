import { createServer, type IncomingMessage, type Server } from 'node:http';
import { AddressInfo } from 'node:net';
import { afterAll, beforeAll, expect, it } from 'vitest';

import { Statoly } from '../src/index.js';

const monitor = {
  id: '6ba7b810-9dad-11d1-80b4-00c04fd430c8',
  title: 'Homepage',
  type: 'http',
  status: 'up',
  active: true,
  metadata: [{ key: 'team', value: 'platform' }],
  createdAt: '2026-01-02T03:04:05Z',
  updatedAt: '2026-01-02T03:05:05Z',
};

let server: Server;
let baseUrl: string;
const received: IncomingMessage[] = [];

beforeAll(async () => {
  server = createServer((request, response) => {
    received.push(request);
    response.writeHead(200, { 'content-type': 'application/json' });
    response.end(JSON.stringify([monitor]));
  });

  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', resolve));

  baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});

afterAll(() => new Promise<void>((resolve) => server.close(() => resolve())));

it('sends the token as a bearer credential and parses the response', async () => {
  const statoly = new Statoly('org_tok_test', { baseUrl });

  const monitors = await statoly.monitors.get();

  expect(received).toHaveLength(1);
  expect(received[0].headers.authorization).toBe('Bearer org_tok_test');
  expect(received[0].url).toBe('/monitors');

  expect(monitors).toHaveLength(1);
  expect(String(monitors![0].id)).toBe(monitor.id);
  expect(monitors![0].title).toBe('Homepage');
  // The spec says date-time, so the client must hand back a Date and not the
  // raw string. This is the shape the DTO layer exists to guarantee.
  expect(monitors![0].createdAt).toBeInstanceOf(Date);
  expect(monitors![0].metadata?.[0]?.key).toBe('team');
});

it('refuses to build a client without a token', () => {
  expect(() => new Statoly('')).toThrow(/token is required/);
});
