import { randomBytes } from 'node:crypto';
import { addDaysTaipei, formatTaipei, taipeiDateKey } from './time.mjs';

export const PRO_FEATURES = Object.freeze(['save_history', 'hosted_quota', 'faster_ui']);
export const GUEST_UPLOADS_LIMIT = 3;
export const DEFAULT_HOSTED_RUNS = 100;
export const DEFAULT_MOCK_USER = Object.freeze({
  id: '1',
  login: 'wids-mock',
  avatar_url: 'https://avatars.githubusercontent.com/u/0?v=4',
});

export function parseMockPlan(value) {
  const plan = (value || '').trim().toLowerCase();
  if (plan === 'free' || plan === 'trial' || plan === 'active') return plan;
  return null;
}

export function parseIdList(value) {
  if (!value) return [];
  return String(value)
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

function newId(prefix) {
  return `${prefix}_${randomBytes(12).toString('base64url')}`;
}

export function createStore(options = {}) {
  const nowFn = options.now || (() => new Date());
  const mockPlan = parseMockPlan(options.mockPlan ?? process.env.MOCK_PLAN);
  const hostedRunsSeed = Number(options.hostedRunsRemaining ?? process.env.MOCK_HOSTED_RUNS ?? DEFAULT_HOSTED_RUNS);
  const forceActiveIds = new Set([
    ...parseIdList(options.forceActiveGithubIds ?? process.env.MOCK_FORCE_ACTIVE_GITHUB_IDS),
  ]);
  const mockUser = {
    ...DEFAULT_MOCK_USER,
    ...(options.mockUser || {}),
  };

  const users = new Map();
  const tokens = new Map();
  const sessions = new Map();
  const history = new Map();
  const guestUploads = new Map();

  function now() {
    return nowFn();
  }

  function isForcedActive(userId) {
    return forceActiveIds.has(String(userId));
  }

  function forceActive(userId) {
    forceActiveIds.add(String(userId));
  }

  function seedEntitlement(userId) {
    if (isForcedActive(userId) || mockPlan === 'active') {
      return {
        plan: 'pro',
        status: 'active',
        trialEndsAt: null,
        validUntil: formatTaipei(addDaysTaipei(now(), 30)),
        hostedRunsRemaining: hostedRunsSeed,
        source: isForcedActive(userId) ? 'manual' : 'mock_plan',
      };
    }
    if (mockPlan === 'free') {
      return {
        plan: 'free',
        status: 'none',
        trialEndsAt: null,
        validUntil: null,
        hostedRunsRemaining: null,
        source: 'mock_plan',
      };
    }
    return {
      plan: 'trial',
      status: 'trialing',
      trialEndsAt: formatTaipei(addDaysTaipei(now(), 7)),
      validUntil: formatTaipei(addDaysTaipei(now(), 7)),
      hostedRunsRemaining: hostedRunsSeed,
      source: mockPlan === 'trial' ? 'mock_plan' : 'trial',
    };
  }

  function getOrCreateUser() {
    let user = users.get(mockUser.id);
    if (!user) {
      const seed = seedEntitlement(mockUser.id);
      user = {
        id: mockUser.id,
        login: mockUser.login,
        avatar_url: mockUser.avatar_url,
        ...seed,
        createdAt: formatTaipei(now()),
      };
      users.set(user.id, user);
      history.set(user.id, []);
    }
    return user;
  }

  function refreshUser(user) {
    if (isForcedActive(user.id)) {
      user.plan = 'pro';
      user.status = 'active';
      user.source = 'manual';
      if (user.hostedRunsRemaining == null) user.hostedRunsRemaining = hostedRunsSeed;
      if (!user.validUntil) user.validUntil = formatTaipei(addDaysTaipei(now(), 30));
      return user;
    }
    if (user.plan === 'trial' && user.status === 'trialing' && user.trialEndsAt) {
      if (now().getTime() > Date.parse(user.trialEndsAt)) {
        user.plan = 'free';
        user.status = 'none';
        user.hostedRunsRemaining = null;
        user.validUntil = null;
        user.source = 'trial_expired';
      }
    }
    return user;
  }

  function featuresFor(user) {
    const live = refreshUser(user);
    if (
      (live.plan === 'trial' && live.status === 'trialing') ||
      (live.plan === 'pro' && live.status === 'active')
    ) {
      return [...PRO_FEATURES];
    }
    return [];
  }

  function guestUsage(guestId) {
    const key = guestId || 'anonymous';
    const today = taipeiDateKey(now());
    const current = guestUploads.get(key);
    if (!current || current.date !== today) {
      const fresh = { date: today, count: 0 };
      guestUploads.set(key, fresh);
      return fresh;
    }
    return current;
  }

  function guestRemaining(guestId) {
    return Math.max(0, GUEST_UPLOADS_LIMIT - guestUsage(guestId).count);
  }

  function entitlementOf(user, guestId) {
    if (!user) {
      return {
        plan: 'free',
        status: 'none',
        features: [],
        quota: {
          guest_uploads_remaining_today: guestRemaining(guestId),
          guest_uploads_limit_per_day: GUEST_UPLOADS_LIMIT,
          hosted_runs_remaining: null,
          seats: 1,
          valid_until: null,
        },
        source: 'anonymous',
        trial_ends_at: null,
      };
    }
    const live = refreshUser(user);
    return {
      plan: live.plan,
      status: live.status,
      features: featuresFor(live),
      quota: {
        guest_uploads_remaining_today: guestRemaining(guestId),
        guest_uploads_limit_per_day: GUEST_UPLOADS_LIMIT,
        hosted_runs_remaining: live.hostedRunsRemaining,
        seats: 1,
        valid_until: live.validUntil,
      },
      source: live.source,
      trial_ends_at: live.trialEndsAt,
    };
  }

  function publicUser(user) {
    return {
      id: user.id,
      login: user.login,
      avatar_url: user.avatar_url,
    };
  }

  function issueToken(user) {
    const token = randomBytes(24).toString('base64url');
    tokens.set(token, user.id);
    return token;
  }

  function userFromToken(token) {
    const userId = tokens.get(token);
    if (!userId) return null;
    const user = users.get(userId);
    return user ? refreshUser(user) : null;
  }

  function loginMockUser() {
    const user = getOrCreateUser();
    const token = issueToken(user);
    return { token, user: refreshUser(user) };
  }

  function createCheckout(user, plan, interval) {
    const session = {
      session_id: newId('cs_mock'),
      user_id: user.id,
      plan,
      interval,
      status: 'open',
      created_at: formatTaipei(now()),
    };
    sessions.set(session.session_id, session);
    return session;
  }

  function getUser(userId) {
    const user = users.get(userId);
    return user ? refreshUser(user) : null;
  }

  function completeCheckout(sessionId) {
    const session = sessions.get(sessionId);
    if (!session) return null;
    const user = users.get(session.user_id);
    if (user) {
      user.plan = 'pro';
      user.status = 'active';
      user.source = 'checkout';
      user.validUntil = formatTaipei(addDaysTaipei(now(), 30));
      if (user.hostedRunsRemaining == null) user.hostedRunsRemaining = hostedRunsSeed;
    }
    session.status = 'completed';
    return { session, user: user ? refreshUser(user) : null };
  }

  function cancelCheckout(sessionId) {
    const session = sessions.get(sessionId);
    if (!session) return null;
    if (session.status === 'open') session.status = 'canceled';
    return session;
  }

  function addHistory(user, item) {
    const list = history.get(user.id) || [];
    const record = {
      id: newId('hist'),
      pattern_id: item.pattern_id,
      source_name: item.source_name,
      row_count: item.row_count,
      note: item.note ?? null,
      created_at: formatTaipei(now()),
    };
    list.unshift(record);
    history.set(user.id, list);
    if (typeof user.hostedRunsRemaining === 'number') {
      user.hostedRunsRemaining = Math.max(0, user.hostedRunsRemaining - 1);
    }
    return record;
  }

  function listHistory(user) {
    return history.get(user.id) || [];
  }

  function consumeGuestUpload(guestId, kind) {
    if (kind === 'demo') {
      return { counted: false, remaining: guestRemaining(guestId) };
    }
    const usage = guestUsage(guestId);
    if (usage.count >= GUEST_UPLOADS_LIMIT) {
      return { counted: false, remaining: 0, exceeded: true };
    }
    usage.count += 1;
    return { counted: true, remaining: guestRemaining(guestId) };
  }

  return {
    mockPlan,
    mockUser,
    now,
    isForcedActive,
    forceActive,
    getOrCreateUser,
    getUser,
    entitlementOf,
    publicUser,
    userFromToken,
    loginMockUser,
    createCheckout,
    completeCheckout,
    cancelCheckout,
    addHistory,
    listHistory,
    guestRemaining,
    consumeGuestUpload,
    featuresFor,
  };
}
