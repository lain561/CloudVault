FROM cgr.dev/chainguard/wolfi-base

ARG version=3.12
WORKDIR /app

RUN apk add python-${version} py${version}-pip && \
	chown -R nonroot.nonroot /app/

# Copy the SSL certificates
COPY certificate.pem /app/
COPY private_key.pem /app/

#USER nonroot
COPY requirements.txt data.py /app/

#uploads directory
RUN mkdir uploads

#copying templates
COPY templates /app/templates/
COPY templates /app/templates/subFolder/

#copying CSS
COPY static /app/static/
COPY static /app/static/fonts

RUN  pip install -r requirements.txt --user

ENTRYPOINT [ "python", "data.py" ]