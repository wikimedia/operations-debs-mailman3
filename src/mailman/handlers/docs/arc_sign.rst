===========
ARC Signing
===========

It is highly recommended that Mailman maintainers configure ARC siging of their
outgoing email.  ARC is the standard protocol for authenticating the content
and authenticity of indirect email flows. These are systems that are more
complex than a basic sender -> reciever flow.  Mailing lists are a primary
example of this.

Configuration is handled in the [ARC] section of ``mailman.cfg``, and is mostly
a question of cryptographic key management.  A public/private key pair should
be generated, and the various options configured. See
http://www.gettingemaildelivered.com/dkim-explained-how-to-set-up-and-use-domainkeys-identified-mail-effectively
for reference, as well as the additional documentaion about ARC configuration
in general in schema.cfg.

The private key should be secured locally and made readable to Mailman, and the
can be specified in ``mailman.cfg``::

  [ARC]
  privkey: /path/to/private.key



The public key should be put into a DNS TXT record, and located at:

#{config.ARC.selector}._domainkey.#{config.ARC.domain}

For example:

test._domainkey.example.com

The following is an example TXT record:
::

    "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCyBwu6PiaDN87t3DVZ84zIrEhCoxtFuv7g52oCwAUXTDnXZ+0XHM/rhkm8XSGr1yLsDc1zLGX8IfITY1dL2CzptdgyiX7vgYjzZqG368C8BtGB5m6nj26NyhSKEdlV7MS9KbASd359ggCeGTT5QjRKEMSauVyVSeapq6ZcpZ9JwQIDAQAB"

The value of the above p= tag should be the public key from your pair.

Enabling signing will result in the addition of three ARC header fields to the
outgoing email, which will be evaluated by the receiver.
