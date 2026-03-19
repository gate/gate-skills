# Gate Growth Referral Skill

## Overview

An invite-friends activity recommendation and rule interpretation skill for Gate platform, covering activity introduction, rule explanation, personalized recommendation, and FAQ handling for three referral programs: Earn Together, Help & Get Coupons, and Super Commission.

### Core Capabilities

- Activity recommendation (check Earn Together status, recommend matching activities)
- Rule interpretation (explain participation steps, reward mechanism, and constraints for each activity)
- Personalized recommendation (quick cash → Earn Together, coupons → Help & Get Coupons, passive income → Super Commission)
- FAQ handling (reward timing, amount differences, task requirements)
- Capability boundary management (data queries redirected to activity page)

## Three Referral Programs

| Program | Type | Reward |
|---------|------|--------|
| Earn Together | Time-limited event | Both parties receive random cash vouchers |
| Help & Get Coupons | Permanent activity | Platform coupon rewards |
| Super Commission | Permanent activity | Ongoing trading fee rebates |

## Architecture

```
gate-growth-referral/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    └── scenarios.md
```

## Usage Examples

```
"What referral activities do you have?"
"How does Earn Together work?"
"I want to earn money quickly. Which activity do you recommend?"
"Can I join all three activities at the same time?"
"When will my reward arrive?"
"How many people have I invited?"
```

## Trigger Phrases

- invite friends / referral / referral reward / invitation campaign
- invite / referral / referral link / referral program
- earn together / limited-time event
- help & get coupons / coupon / trial voucher / discount coupon
- super commission / commission / rebate / passive income
- how to earn / invitation reward / how to invite
