import{generateSecretKey,getPublicKey,finalizeEvent,verifyEvent,getEventHash}from"nostr-tools/pure";
import*as nip44 from"nostr-tools/nip44";import*as nip19 from"nostr-tools/nip19";
import qrcode from"qrcode-generator";import jsQR from"jsqr";
window.NT={generateSecretKey,getPublicKey,finalizeEvent,verifyEvent,getEventHash,nip44,nip19};window.QR=qrcode;window.jsQR=jsQR;
