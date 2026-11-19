# Model comparison: SAFE contract summaries

Instruction given to every model: "Write a one-paragraph synthesis of this contract in 100 words."

I judged quality by reading the summaries myself, not with an eval.

## Haiku (`claude-haiku-5-5`): 100 words, 2824 output tokens, 10.6s

YayYo, Inc., a Delaware corporation, issues this Simple Agreement for Future Equity (SAFE) for an investor's Purchase Amount, granting the right to receive SAFE Preferred Stock that accrues an 8% annual dividend. The conversion discount depends on the Sale Date: 50% through December 31, 2016, declining to 10% by February 15, 2017, and none thereafter. Shares convert automatically upon a Regulation A+ or IPO equity financing. In liquidity events, the investor may elect cash or shares. If no financing occurs by December 31, 2017, forced conversion applies, subject to a $50 million cap. The agreement is governed by California law.

## Sonnet (`claude-sonnet-5-5`): 99 words, 1527 output tokens, 10.3s

This SAFE (Simple Agreement for Future Equity) is a YayYo, Inc. private placement of up to $5 million in convertible preferred stock rights, accruing 8% annual dividends. Investors pay the purchase amount within two business days and receive conversion shares at a discount of 10–50% to the Regulation A+ offering price, depending on purchase date. Conversion occurs upon an equity financing, or automatically by December 31, 2017 under a $50 million valuation cap. Liquidity or dissolution events trigger priority cash repayment. The agreement includes securities-law representations, investor accreditation certifications, Regulation S provisions, anti-money-laundering requirements, California law, and jury waiver.

## Opus (`claude-opus-5-5`): 101 words, 1189 output tokens, 10.7s

This Simple Agreement for Future Equity (SAFE) lets an investor fund YayYo, Inc., in a private placement of up to $5 million under Regulation D and/or Regulation S. Investments accrue an 8% annual dividend and convert into common stock at a discount to the price of YayYo's Regulation A+ offering or IPO; discounts fall from 50% to zero depending on purchase date. Upon a change of control, investors may take cash or shares; upon dissolution, they receive repayment plus dividends before stockholders. Absent any event by December 31, 2017, conversion is forced under a $50 million valuation cap. California law governs.

## Fable (`claude-fable-5-2`): 100 words, 1374 output tokens, 12.1s

This Simple Agreement for Future Equity lets an investor fund YayYo, Inc. in a private placement of up to $5 million, in exchange for the right to SAFE Preferred Stock convertible into common shares. The purchase amount accrues an 8% annual dividend and converts upon a Regulation A+ offering or IPO at a discount of 50% to zero, depending on investment date. Investors may take cash or shares in a change of control, receive priority repayment upon dissolution, and face forced conversion if no triggering event occurs by December 31, 2017. The unregistered securities carry transfer restrictions; California law governs.

## Haiku (`claude-haiku-5-5`, thinking off): 120 words, 279 output tokens, 1.8s

This is a Simple Agreement for Future Equity (SAFE) issued by YayYo, Inc., a Delaware corporation, under Regulation A+ (Tier 2) and Rule 506/Regulation S exemptions. The Investor pays a Purchase Amount in exchange for the right to receive SAFE Preferred Stock that converts into common stock at a discount (50% to 0%, depending on how early the investment is made) upon an Equity Financing, cash-out or stock conversion upon a Liquidity Event, or payout upon a Dissolution Event, with a forced conversion by December 31, 2017 subject to a $50 million valuation cap. The instrument accrues an 8% annual dividend, is unregistered and subject to resale restrictions, and includes investor accreditation certifications, anti-money laundering forms, and California governing law.

## Sonnet (`claude-sonnet-5-5`, thinking off (between_tools)): 103 words, 228 output tokens, 2.2s

This YayYo, Inc. SAFE (Simple Agreement for Future Equity) lets an investor fund the company in exchange for a right to SAFE Preferred Stock, accruing an 8% annual dividend. The stock converts into common shares at a discount (50% to 10%, depending on the purchase date) to the Regulation A+ offering price. Conversion is triggered by an equity financing, or by a forced conversion after December 31, 2017, subject to a $50 million valuation cap. Investors may receive cash or shares upon a liquidity event, and get priority payment upon dissolution. The document includes securities-law representations, investor accreditation certifications, and anti-money laundering requirements.

## Opus (`claude-opus-5-5`, effort low (can't turn off)): 103 words, 224 output tokens, 3.3s

This Simple Agreement for Future Equity (SAFE) lets investors buy rights to YayYo, Inc.'s SAFE Preferred Stock in a private placement of up to $5 million. The purchase amount accrues 8% annual dividends. Upon an Equity Financing (a Regulation A+ offering or IPO), investments convert into common stock at a discount of 0–50%, depending on how early the investor purchased. If a Change of Control occurs, investors may take cash or shares. In a dissolution, they receive repayment ahead of other stockholders. Absent any of these events by December 31, 2017, conversion is forced at a $50 million valuation cap. California law governs.

## Fable (`claude-fable-5-2`, effort low (can't turn off)): 102 words, 224 output tokens, 2.7s

This Simple Agreement for Future Equity (SAFE) between YayYo, Inc., a Delaware corporation, and an investor grants rights to SAFE Preferred Stock, accruing 8% annual dividends, as part of a private placement of up to $5,000,000. On an equity financing (Regulation A+ offering or IPO), the purchase amount plus dividends converts automatically into common stock at a discount of 50% to 0%, depending on the investment date. Investors may take cash or shares on a liquidity event, have priority in dissolution, and face forced conversion if no event occurs by December 31, 2017. The unregistered securities carry transfer restrictions; California law governs.
