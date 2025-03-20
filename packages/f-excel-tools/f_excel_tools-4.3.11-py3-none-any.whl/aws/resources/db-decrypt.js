#!/usr/bin/env node

/* Note: this script is a demo only file that sets the aws encryption framework with some environment KMS keys
*  Then if tries to decrypt using those keys a given content
*/

/* Based on: https://www.npmjs.com/package/@aws-crypto/client-node */

const { KmsKeyringNode, buildClient, CommitmentPolicy } = require('@aws-crypto/client-node');

/* Retrieve the Base64-encoded encrypted content from command-line arguments */
const encryptedBase64 = process.argv[2];
if (!encryptedBase64) {
    console.error('Usage: node db-decrypt.js <base64_encrypted_content>');
    process.exit(1);
}

/* Decode the Base64 string into a Buffer */
const encryptedData = Buffer.from(encryptedBase64, 'base64');

/* Start by constructing a keyring. We'll create a KMS keyring.
 * Specify an AWS Key Management Service (AWS KMS) customer master key (CMK) to be the
 * generator key in the keyring. This CMK generates a data key and encrypts it.
 * To use the keyring to encrypt data, you need kms:GenerateDataKey permission
 * on this CMK. To decrypt, you need kms:Decrypt permission.
 */
const generatorKeyId = process.env.FIELD_LEVEL_KMS_DATA_ENCRYPTION_ARN;
if (!generatorKeyId) {
    console.error('Error: FIELD_LEVEL_KMS_DATA_ENCRYPTION_ARN environment variable is not set.');
    process.exit(1);
}

/* You can specify additional CMKs for the keyring. The data key that the generator key
 * creates is also encrypted by the additional CMKs you specify. To encrypt data,
 *  you need kms:Encrypt permission on this CMK. To decrypt, you need kms:Decrypt permission.
 */
const keyIds = [
    process.env.TRANSACTION_KMS_KEY,
    process.env.MAIN_REGION_FIELD_LEVEL_KMS_DATA_ENCRYPTION_ARN,
].filter(Boolean);

/* Create the KMS keyring */
const keyring = new KmsKeyringNode({
    generatorKeyId,
    keyIds,
});

const { decrypt } = buildClient(CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT);

(async () => {
    try {
        /* Decrypt the result using the same keyring */
        const { plaintext, messageHeader } = await decrypt(keyring, encryptedData);

        /* Get the encryption context */
        const { encryptionContext } = messageHeader

        /* Verify that all values in the original encryption context are in the
         * current one. (The Encryption SDK adds extra values for signing.)
         */
        // Object
        //     .entries(context)
        //     .forEach(([key, value]) => {
        //         if (encryptionContext[key] !== value) throw new Error('Encryption Context does not match expected values')
        //     })

        console.log('Encryption Context:', JSON.stringify(encryptionContext, null, 2));
        console.log('Decrypted Content:', JSON.stringify(JSON.parse(plaintext.toString()), null, 2) );
    } catch (error) {
        console.error('Decryption failed:', error);
    }
})();
