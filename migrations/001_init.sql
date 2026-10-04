create table notifications (
    id uuid primary key default gen_random_uuid(),
    user_id text not null,
    order_id text not null,
    kind text not null,
    title text not null,
    body text not null,
    channel text not null default 'in_app',
    status text not null default 'delivered',
    created_at timestamptz not null default now(),
    unique (order_id, kind)
);

create index notifications_user on notifications (user_id, created_at desc);
