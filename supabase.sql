create extension if not exists pgcrypto;

create table if not exists public.alerts (
    id uuid primary key default gen_random_uuid(),
    email text not null,
    asset text not null default 'BTC',
    direction text not null check (direction in ('above', 'below')),
    price_threshold numeric not null,
    custom_message text,
    cooldown_minutes integer not null default 60,
    last_sent_at timestamptz,
    enabled boolean not null default true,
    created_at timestamptz not null default now()
);

create index if not exists alerts_asset_idx on public.alerts (asset);
create index if not exists alerts_enabled_idx on public.alerts (enabled);
