
import * as anchor from '@coral-xyz/anchor'
import { Program } from '@coral-xyz/anchor'
import { PublicKey, clusterApiUrl, Connection, Keypair, TransactionSignature, TransactionInstruction, Transaction } from '@solana/web3.js'
import { Vault } from '../target/types/vault'
import * as spl from '@solana/spl-token';
import { expect, use } from 'chai'
import { AnchorProvider, Provider, web3 } from '@project-serum/anchor';
import { token } from '@project-serum/anchor/dist/cjs/utils';

//VDfDMRUDsgAP2qR8K6DUPn7Lw9586g86PtMjazPdvf3 admin
describe("vault",  () => {
  // Configure the client to use the local cluster.
  // anchor.setProvider(anchor.AnchorProvider.env());
  const TOKEN_PROGRAM_ID = new PublicKey(
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
  );
   const ASSOCIATED_PROGRAM_ID = new PublicKey(
    "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
  );
  const provider = anchor.AnchorProvider.env()

  anchor.setProvider(provider)
  
  Keypair.generate()
  // let admin:anchor.web3.Keypair = anchor.web3.Keypair.generate()
  // let dummy:anchor.web3.Keypair = anchor.web3.Keypair.generate()
  const program = anchor.workspace.Vault as Program<Vault>;
  //181 = 8kk
    let admin:anchor.web3.Keypair = anchor.web3.Keypair.generate()
    let user_account:anchor.web3.Keypair = anchor.web3.Keypair.generate()

  // console.log("provider ", provider.publicKey)
  // console.log("8KKk ", EightKK.publicKey) user_account
  // console.log("5oar ", EightKK2.publicKey) dummy

  let authorityAccount:anchor.web3.Keypair = anchor.web3.Keypair.generate();
  let user_token_a_account;
  let admin_token_a_account;
  let amountInVault;
  let amountInWallet;
  let amountInAdminWallet;
  let admin_token_b_account;
  let user_token_b_account;
  let dummyTokenAccount;
  
  let token_a_mint;
  let token_b_mint;
  const tokenAccountInfo = async (address) => await spl.getAccount(
    provider.connection,
    address
  )
  const create_mint = async (user: Keypair):Promise<PublicKey> => {
    return await spl.createMint(
      provider.connection,
      user,                  //payer
      authorityAccount.publicKey,    //mint auth
      null,                         //freeze auth
      0,
    );
  }

  const get_token_account = async (user:Keypair, mint:PublicKey): Promise<spl.Account> => {
    return await spl.getOrCreateAssociatedTokenAccount(
      provider.connection,
      user,
      mint,
      user.publicKey
    )
  }

  const mint_tokens = async (user: Keypair, mint:PublicKey, tokenAccount:spl.Account): Promise<TransactionSignature> => {
    return await spl.mintTo(
      provider.connection,
      user,
      mint,
      tokenAccount.address,
      authorityAccount,
      100
    )
  }

  const create_user_stats = async (user: Keypair, mint: PublicKey, deposit: PublicKey, ):Promise<TransactionInstruction> => {
    return await program.methods
    .createUserStats(mint, user.publicKey)
    .accounts({
      payer: user.publicKey,
      mint: mint,
      depositInfo: deposit,
      systemProgram: anchor.web3.SystemProgram.programId,
    })
    .signers([user])
    .instruction()
  } 

  const fetch_info_vault = async ( pda: PublicKey) => {
    return await program.account.depositInfo.fetch(pda)
  }

  const fetch_info_admin = async (pda: PublicKey) => {
    return await program.account.adminData.fetch(pda)
  }

  const set_admin = async (pda: PublicKey, admin: Keypair): Promise<TransactionSignature> => {
    return await program.methods
    .setAdmin(admin.publicKey)
    .accounts({
      adminData: pda,
      admin: admin.publicKey,
      systemProgram: anchor.web3.SystemProgram.programId
    })
    .signers([admin])
    .rpc()
  }

  const deposit_user = async (bump: number, amount: number, pdaVault: PublicKey, user: Keypair, tokenAccount: spl.Account, mint: PublicKey, pdaDep: PublicKey):Promise<TransactionInstruction> => {
    return await program.methods
    .deposit(bump, new anchor.BN(amount))
    .accounts({
        vaultAccount:           pdaVault,
        payer:                  user.publicKey,
        payerTokenAccount:      tokenAccount.address,
        mint:                   mint,
        depositInfo:            pdaDep,
        systemProgram:          anchor.web3.SystemProgram.programId,
        tokenProgram:           TOKEN_PROGRAM_ID,
        associatedTokenProgram: ASSOCIATED_PROGRAM_ID
      })
    .signers([user, ])
    .instruction()
  }

  const withdraw_user = async (bump: number, amount: number, pdaVault: PublicKey, user: Keypair, tokenAccount: spl.Account, mint: PublicKey, pdaDep: PublicKey): Promise<TransactionInstruction> => {
    return await program.methods
    .withdraw(bump, new anchor.BN(amount),)
    .accounts({
        vaultAccount:           pdaVault,
        payer:                  user.publicKey,
        payerTokenAccount:      tokenAccount.address,
        mint:                   mint,
        depositInfo:            pdaDep,
        systemProgram:          anchor.web3.SystemProgram.programId,
        tokenProgram:           TOKEN_PROGRAM_ID,
        associatedTokenProgram: ASSOCIATED_PROGRAM_ID
      })
    .signers([user])
    .instruction()
  };

  const deposit_admin = async (bump: number, amount: number, user:PublicKey, pdaVault: PublicKey, pdaAdmin: PublicKey, admin: Keypair, tokenAccount: spl.Account, mint: PublicKey, pdaDep: PublicKey):Promise<TransactionInstruction>  => {
    return await program.methods
    .depositAdmin(bump, new anchor.BN(amount), mint, user)
    .accounts({
        vaultAccount:           pdaVault,
        admin:                  admin.publicKey,
        adminData:              pdaAdmin,
        adminTokenAccount:      tokenAccount.address,
        mint:                   mint,
        depositInfo:            pdaDep,
        systemProgram:          anchor.web3.SystemProgram.programId,
        tokenProgram:           TOKEN_PROGRAM_ID,
        associatedTokenProgram: ASSOCIATED_PROGRAM_ID
      })
    .signers([admin, ])
    .instruction()
  }

  const withdraw_admin = async (bump: number, amount: number, user:PublicKey, pdaVault: PublicKey, pdaAdmin: PublicKey, admin: Keypair, tokenAccount: spl.Account, mint: PublicKey, pdaDep: PublicKey): Promise<TransactionInstruction>  => {
    return await program.methods
    .withdrawAdmin(bump, new anchor.BN(amount), mint, user)
    .accounts({
        vaultAccount:           pdaVault,
        adminData:              pdaAdmin,
        admin:                  admin.publicKey,
        adminTokenAccount:      tokenAccount.address,
        mint:                   mint,
        depositInfo:            pdaDep,
        systemProgram:          anchor.web3.SystemProgram.programId,
        tokenProgram:           TOKEN_PROGRAM_ID,
        associatedTokenProgram: ASSOCIATED_PROGRAM_ID
      })
    .signers([admin])
    .instruction()
  };
  

  it('Deposits Token A!', async () => {
    //mint 100 test tokens in our test users token account
    token_a_mint = await create_mint(user_account);
    token_b_mint = await create_mint(admin)

    user_token_a_account = await get_token_account(user_account, token_a_mint);
    admin_token_a_account = await get_token_account(admin, token_a_mint)
    admin_token_b_account = await get_token_account(admin, token_b_mint)
    user_token_b_account = await get_token_account(user_account, token_b_mint)

    console.log("user tokenaccount: ", user_token_a_account.address)
    var mint_tx_user = await mint_tokens(user_account, token_a_mint, user_token_a_account);
    console.log("mint_tx_user: ", mint_tx_user)

    //mint 100 test tokens in our test users token account
    console.log("admin address: ", admin.publicKey)
    console.log("user token_a_mint: ", token_b_mint)
    
    console.log("user token2account: ", user_token_b_account.address)
    console.log("admin token2account: ", admin_token_b_account.address)
    var mint_tx_admin = await mint_tokens(admin, token_b_mint, admin_token_b_account,)
    console.log("mint_tx_admin: ", mint_tx_admin)

    let [pda_token_a_vault, pda_token_a_vault_bump] = PublicKey.findProgramAddressSync([token_a_mint.toBuffer()], program.programId)
    let [pda_dep_info_token_a, pda_dep_info_token_a_bump] = PublicKey.findProgramAddressSync([anchor.utils.bytes.utf8.encode('user-stats'), user_account.publicKey.toBuffer(), token_a_mint.toBuffer()],program.programId)
    let [pda_token_b_vault, pda_token_b_vault_bump] = PublicKey.findProgramAddressSync([token_b_mint.toBuffer()], program.programId)  
    let [pda_dep_info_token_b, pda_dep_info_token_b_bump] = PublicKey.findProgramAddressSync([anchor.utils.bytes.utf8.encode('user-stats'), user_account.publicKey.toBuffer(), token_b_mint.toBuffer()],program.programId)

    let [pda_admin_data, pda_admin_data_bump] = PublicKey.findProgramAddressSync([anchor.utils.bytes.utf8.encode('admin-data'), admin.publicKey.toBuffer(),],program.programId)
    console.log("pda_admin_data: ", pda_admin_data)

    var tx_user_first_interaction = new Transaction;
    var tx_admin_first_interaction = new Transaction;
    var tx_user_second_interaction = new Transaction;
    const tx_create_user_dep1 = await create_user_stats(user_account, token_a_mint, pda_dep_info_token_a,);
    const tx_create_user_dep2 = await create_user_stats(user_account, token_b_mint, pda_dep_info_token_b)

    const tx_user_dep_token_a = await deposit_user(pda_token_a_vault_bump, 22, pda_token_a_vault, user_account, user_token_a_account, token_a_mint, pda_dep_info_token_a);
    console.log("tx_user_dep_token_a: ")

    tx_user_first_interaction = tx_user_first_interaction.add(tx_create_user_dep1).add(tx_create_user_dep2).add(tx_user_dep_token_a)
      
    console.log(await provider.sendAndConfirm(tx_user_first_interaction, [user_account]))
    
    amountInVault = (await tokenAccountInfo(pda_token_a_vault)).amount.toString();
    amountInWallet = (await tokenAccountInfo(user_token_a_account.address)).amount.toString();
    expect(amountInVault).to.equal("22")
    expect(amountInWallet).to.equal("78")
    console.log("user interaction Executed Successfully");

    // let fetch_user_dep1_after_init = await fetch_info_vault(pda_dep_info_token_a);
    // expect(JSON.stringify(fetch_user_dep1_after_init.userId)).to.equal(
    //   JSON.stringify(user_account.publicKey)
    // )

    // const txSetAdmin = await set_admin(pda_admin_data, admin)

    // let fetch_admin = await fetch_info_admin(pda_admin_data)
    // expect(JSON.stringify(fetch_admin.admin)).to.equal(
    //   JSON.stringify(admin.publicKey)
    // )

    
    // let fetch_user_dep1_again = await fetch_info_vault(pda_dep_info_token_a);
    
  //////////////////////////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////////////////////////

    const tx_admin_withd_token_a = await withdraw_admin(pda_token_a_vault_bump, 10, user_account.publicKey, pda_token_a_vault, pda_admin_data, admin, admin_token_a_account, token_a_mint, pda_dep_info_token_a)
    // console.log("tx_admin_withd_token_a: ", tx_admin_withd_token_a)
    
    // let fetch_user_dep1_after_admin_withd = await fetch_info_vault(pda_dep_info_token_a);
    // console.log("token info:", fetch_user_dep1_after_admin_withd.tokenAmount)

          
    // console.log("tx_create_user_dep1: ", tx_create_user_dep2)
    // let qCreate2Dep = await fetch_info_vault(pda_dep_info_token_b)
      
    const tx_admin_dep_token_b = await deposit_admin(pda_token_b_vault_bump, 30, user_account.publicKey, pda_token_b_vault, pda_admin_data, admin, admin_token_b_account, token_b_mint, pda_dep_info_token_b);
    
    tx_admin_first_interaction = tx_admin_first_interaction.add(tx_admin_withd_token_a).add(tx_admin_dep_token_b);
    console.log(await provider.sendAndConfirm(tx_admin_first_interaction, [admin]))
    
    amountInVault = (await tokenAccountInfo(pda_token_a_vault)).amount.toString();
    amountInAdminWallet = (await tokenAccountInfo(admin_token_a_account.address)).amount.toString();
    expect(amountInVault).to.equal("12")
    expect(amountInAdminWallet).to.equal("10")

    // console.log("tx:", tx_admin_dep_token_b)
    amountInVault = (await tokenAccountInfo(pda_token_b_vault)).amount.toString();
    amountInAdminWallet = (await tokenAccountInfo(admin_token_b_account.address)).amount.toString();
    expect(amountInVault).to.equal("30")
    expect(amountInAdminWallet).to.equal("70")
    // let qD2 = await fetch_info_vault(pda_dep_info_token_b)
    // console.log("token info:", qD2.tokenAmount)
    console.log("Admin interaction Executed Successfully");


    const tx_user_withd_token_b = await withdraw_user(pda_token_b_vault_bump, 5, pda_token_b_vault, user_account, user_token_b_account, token_b_mint, pda_dep_info_token_b );
    
    tx_user_second_interaction.add(tx_user_withd_token_b)
    console.log(await provider.sendAndConfirm(tx_user_second_interaction, [user_account]))

    const tx_admin_withd_token_b_to_user = await withdraw_admin(pda_token_b_vault_bump, 7, user_account.publicKey, pda_token_b_vault, pda_admin_data, admin, user_token_b_account, token_b_mint, pda_dep_info_token_b);
    var tx_admin_second_interaction = new Transaction;
    tx_admin_second_interaction.add(tx_admin_withd_token_b_to_user)
    console.log(await provider.sendAndConfirm(tx_admin_second_interaction, [admin]))
    // console.log("tx_user_withd_token_b: ", tx_user_withd_token_b)
    // console.log(await fetch_info_vault(pda_dep_info_token_b));
    amountInVault = (await tokenAccountInfo(pda_token_b_vault)).amount.toString();
    expect(amountInVault).to.equal("18")
    amountInWallet = (await tokenAccountInfo(user_token_b_account.address)).amount.toString();
    expect(amountInWallet).to.equal("12")
    const amountInWallet2 = (await tokenAccountInfo(user_token_a_account.address)).amount.toString();
    expect(amountInWallet2).to.equal("78")
    const amountInVault2 = (await tokenAccountInfo(pda_token_a_vault)).amount.toString();
    expect(amountInVault2).to.equal("12")

    console.log("User Withdrawal Executed Successfully");
    
    // let qW_u = await fetch_info_vault(pda_dep_info_token_b);
    // console.log(qW_u)
  })
})



