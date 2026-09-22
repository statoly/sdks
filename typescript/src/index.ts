/**
 * Official TypeScript client for the Statoly API.
 *
 * Everything under `./generated` is produced by Kiota from the OpenAPI
 * document and must not be edited. This file is the hand-written surface: it
 * wires the bearer token and the default base URL so callers never touch
 * Kiota's request adapter.
 */
import {
  AllowedHostsValidator,
  BaseBearerTokenAuthenticationProvider,
  type AccessTokenProvider,
} from '@microsoft/kiota-abstractions';
import { DefaultRequestAdapter } from '@microsoft/kiota-bundle';

import { createStatolyClient, type StatolyClient } from './generated/statolyClient.js';

export * from './generated/models/index.js';
export type { StatolyClient };

/** Base URL of the production API. */
export const DEFAULT_BASE_URL = 'https://api.statoly.ch/v1';

export interface StatolyOptions {
  /** Overrides the API the client talks to. Useful for staging. */
  baseUrl?: string;
}

/**
 * Hands the same token to every request.
 *
 * Statoly issues long-lived organization tokens (`org_tok_…`), so there is
 * nothing to refresh. An empty AllowedHostsValidator means the token travels
 * to whatever baseUrl the caller configured, including a local stub.
 */
class StaticTokenProvider implements AccessTokenProvider {
  private readonly validator = new AllowedHostsValidator();

  constructor(private readonly token: string) {}

  public getAuthorizationToken(): Promise<string> {
    return Promise.resolve(this.token);
  }

  public getAllowedHostsValidator(): AllowedHostsValidator {
    return this.validator;
  }
}

/**
 * A client for one Statoly organization.
 *
 * ```ts
 * const statoly = new Statoly(process.env.STATOLY_TOKEN!);
 * const monitors = await statoly.monitors.get();
 * ```
 */
export class Statoly {
  /** The generated fluent API, for anything this wrapper does not surface. */
  public readonly api: StatolyClient;

  constructor(token: string, options: StatolyOptions = {}) {
    if (!token) {
      throw new Error('Statoly: an organization token is required');
    }

    const adapter = new DefaultRequestAdapter(
      new BaseBearerTokenAuthenticationProvider(new StaticTokenProvider(token)),
    );

    adapter.baseUrl = options.baseUrl ?? DEFAULT_BASE_URL;

    this.api = createStatolyClient(adapter);
  }

  /** `/monitors` and everything below it. */
  public get monitors() {
    return this.api.monitors;
  }
}
