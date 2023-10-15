use anchor_lang::prelude::*;
use anchor_spl::{
    associated_token::AssociatedToken,
    token::{Mint, Token, TokenAccount},
};

declare_id!("AvyqWo2UHmAnn6KLqL5SVZk7UyeVco1Bgim6PosNVvvH");


#[program]
pub mod vault {
    use super::*;

    pub fn create_user_stats(ctx: Context<CreateDepositInfo>, _mint: Pubkey, _user_id: Pubkey, ) -> Result<()> {
        let deposit_info = &mut ctx.accounts.deposit_info;
        deposit_info.user_id = _user_id;
        deposit_info.mint = _mint;
        deposit_info.token_amount = 0;

        Ok(())
    }
    // pub fn create_user_stats_for(ctx: Context<CreateDepositInfoFor>, _mint: Pubkey, _user_id: Pubkey) -> Result<()> {
    //     let deposit_info = &mut ctx.accounts.deposit_info;
    //     deposit_info.user_id = _user_id;
    //     deposit_info.mint = _mint;
    //     deposit_info.token_amount = 0;
    //     Ok(())
    // }

    pub fn set_admin(ctx: Context<SetAdmin>, _admin: Pubkey) -> Result<()> {
        let state = &mut ctx.accounts.admin_data;
        state.admin = _admin;
        Ok(())
    }

    pub fn change_admin(ctx: Context<ChangeAdmin>, new_admin: Pubkey) -> Result<()> {
        let state = &mut ctx.accounts.admin_data;
        state.admin = new_admin;
        Ok(())
    }

    pub fn deposit(ctx: Context<Deposit>, _bump: u8, amount: u64) -> Result<()> {
        anchor_spl::token::transfer(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                anchor_spl::token::Transfer {
                    from: ctx
                        .accounts
                        .payer_token_account
                        .to_account_info(),
                    to: ctx
                        .accounts
                        .vault_account
                        .to_account_info(),
                    authority: ctx.accounts.payer.to_account_info(),
                },
            ),
            amount,
        );
        let deposit_info = &mut ctx.accounts.deposit_info;
        deposit_info.token_amount += amount;

        Ok(())
    }

    pub fn withdraw(ctx: Context<Withdraw>, bump: u8, amount: u64) -> Result<()> {
        require!(ctx.accounts.deposit_info.token_amount >= amount, MyError::RequireViolated);
        ctx.accounts.deposit_info.token_amount -= amount;
        anchor_spl::token::transfer(
            CpiContext::new_with_signer(
                ctx.accounts.token_program.to_account_info(),
                anchor_spl::token::Transfer {
                    from: ctx
                        .accounts
                        .vault_account
                        .to_account_info(),
                    to: ctx
                        .accounts
                        .payer_token_account
                        .to_account_info(),
                    authority: ctx.accounts.vault_account.to_account_info(),
                },
                &[&[ ctx.accounts.mint.key().as_ref(),&[bump], ]],
            ),
            amount,
        );
        Ok(())
    }

    pub fn withdraw_admin(ctx: Context<WithdrawAdmin>, bump: u8, amount: u64, _mint: Pubkey, _user_id: Pubkey) -> Result<()> {
        require!(ctx.accounts.deposit_info.token_amount >= amount, MyError::RequireViolated);
        require!(ctx.accounts.deposit_info.mint == _mint, MyError::RequireViolated);
        require!(ctx.accounts.deposit_info.user_id == _user_id, MyError::RequireViolated);

        ctx.accounts.deposit_info.token_amount -= amount;
        anchor_spl::token::transfer(
            CpiContext::new_with_signer(
                ctx.accounts.token_program.to_account_info(),
                anchor_spl::token::Transfer {
                    from: ctx
                        .accounts
                        .vault_account
                        .to_account_info(),
                    to: ctx
                        .accounts
                        .admin_token_account
                        .to_account_info(),
                    authority: ctx.accounts.vault_account.to_account_info(),
                },
                &[&[
                    ctx.accounts.mint.key().as_ref(),
                    &[bump],
                ]],
            ),
            amount,
        );
        Ok(())
    }

    pub fn deposit_admin(ctx: Context<DepositAdmin>, _bump: u8, amount: u64, _mint: Pubkey, _user_id: Pubkey) -> Result<()> {
        require!(ctx.accounts.deposit_info.mint == _mint, MyError::RequireViolated);
        require!(ctx.accounts.deposit_info.user_id == _user_id, MyError::RequireViolated);

        anchor_spl::token::transfer(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                anchor_spl::token::Transfer {
                    from: ctx
                        .accounts
                        .admin_token_account
                        .to_account_info(),
                    to: ctx
                        .accounts
                        .vault_account
                        .to_account_info(),
                    authority: ctx.accounts.admin.to_account_info(),
                },
            ),
            amount,
        );
        let deposit_info = &mut ctx.accounts.deposit_info;
        deposit_info.token_amount += amount;

        Ok(())
    }
}

#[account]
pub struct AdminData {
    pub admin: Pubkey,
}
#[account]
pub struct DepositInfo {
    pub user_id: Pubkey,
    pub mint: Pubkey,
    pub token_amount: u64,
    bump: u8
}

#[derive(Accounts)]
pub struct SetAdmin<'info> {
    #[account(mut)]
    pub admin: Signer<'info>,
    #[account(
        init, 
        payer = admin, 
        space = 800, 
        seeds = [b"admin-data", admin.key().as_ref()], 
        bump
    )]
    pub admin_data: Account<'info, AdminData>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct ChangeAdmin<'info> {
    #[account(mut, has_one = admin)]
    pub admin_data: Account<'info, AdminData>,
    pub admin: Signer<'info>,
}

#[derive(Accounts)]
pub struct CreateDepositInfo<'info> {
    #[account(mut)]
    pub payer: Signer<'info>,
    pub mint: Account<'info, Mint>,
    #[account(
        init,
        payer = payer,
        space = 800, 
        seeds = [b"user-stats", payer.key().as_ref(), mint.key().as_ref()], 
        bump
    )]
    pub deposit_info: Account<'info, DepositInfo>,
    pub system_program: Program<'info, System>,
}

// #[derive(Accounts)]
// #[instruction(_user_id: Pubkey)]
// pub struct CreateDepositInfoFor<'info> {
//     #[account(mut, has_one = admin)]
//     pub admin_data: Account<'info, AdminData>,
//     #[account(mut)]
//     pub admin: Signer<'info>,
//     pub mint: Account<'info, Mint>,
//     #[account(
//         init,
//         payer = admin,
//         space = 200, 
//         seeds = [b"user-stats", _user_id.as_ref(), mint.key().as_ref()], 
//         bump
//     )]
//     pub deposit_info: Account<'info, DepositInfo>,
//     pub system_program: Program<'info, System>,
// }

#[derive(Accounts)]
pub struct Deposit<'info> {
    #[account(
        init_if_needed,
        payer = payer,
        seeds = [mint.key().as_ref()],
        bump,
        token::mint = mint,
        token::authority = vault_account,
    )]
    pub vault_account: Account<'info, TokenAccount>,
    #[account(mut)]
    pub payer: Signer<'info>,
    #[account(mut)]
    pub payer_token_account: Account<'info, TokenAccount>,
    pub mint: Account<'info, Mint>,
    #[account(
        mut,
        seeds = [b"user-stats", payer.key().as_ref(), mint.key().as_ref()], 
        bump
    )]
    pub deposit_info: Account<'info, DepositInfo>,
    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
    pub associated_token_program: Program<'info, AssociatedToken>,
}

#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(mut)]
    pub vault_account: Account<'info, TokenAccount>,
    #[account(mut)]
    pub payer: Signer<'info>,
    #[account(mut)]
    pub payer_token_account: Account<'info, TokenAccount>,
    pub mint: Account<'info, Mint>,
    #[account(
        mut,
        seeds = [b"user-stats", payer.key().as_ref(), mint.key().as_ref()], 
        bump 
    )]
    pub deposit_info: Account<'info, DepositInfo>,
    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
    pub associated_token_program: Program<'info, AssociatedToken>,
}

#[derive(Accounts)]
pub struct WithdrawAdmin<'info> {
    #[account(mut)]
    pub vault_account: Account<'info, TokenAccount>,
    #[account(has_one = admin)]
    pub admin_data: Account<'info, AdminData>,
    pub admin: Signer<'info>,
    #[account(mut)]
    pub admin_token_account: Account<'info, TokenAccount>,
    pub mint: Account<'info, Mint>,
    #[account(mut)]
    pub deposit_info: Account<'info, DepositInfo>,
    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
    pub associated_token_program: Program<'info, AssociatedToken>,
}

#[derive(Accounts)]
pub struct DepositAdmin<'info> {
    #[account(
        init_if_needed,
        payer = admin,
        seeds = [mint.key().as_ref()],
        bump,
        token::mint = mint,
        token::authority = vault_account,
    )]
    pub vault_account: Account<'info, TokenAccount>,
    #[account(has_one = admin)]
    pub admin_data: Account<'info, AdminData>,
    #[account(mut)]
    pub admin: Signer<'info>,
    #[account(mut)]
    pub admin_token_account: Account<'info, TokenAccount>,
    pub mint: Account<'info, Mint>,
    #[account(mut)]
    pub deposit_info: Account<'info, DepositInfo>,
    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
    pub associated_token_program: Program<'info, AssociatedToken>,
}

#[error_code]
pub enum MyError {
    #[msg("Insuffiecient amount of tokens")]
    RequireViolated
}