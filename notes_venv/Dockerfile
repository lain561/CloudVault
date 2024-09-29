FROM cgr.dev/chainguard/wolfi-base

ARG version=3.12
WORKDIR /app

# Define the volume
VOLUME ["/app/Vuploads"]

RUN apk add python-${version} py${version}-pip && \
	chown -R nonroot.nonroot /app/

# Copy the SSL certificates
COPY certificate.pem /app/
COPY private_key.pem /app/

#minimum permissions to run
USER nonroot

#copy the requirements that are only needed 
COPY requirements.txt data.py /app/

#uploads directory
RUN mkdir uploads

#copying templates
COPY templates /app/templates/
COPY templates /app/templates/subFolder/

#copying CSS
COPY static/css /app/static/css/
COPY static/images /app/static/images/
COPY static/css/fonts /app/static/css/fonts/

#health check
HEALTHCHECK CMD curl --fail http://localhost:8080/health || exit 1

#only install the files needed
RUN  pip install -r requirements.txt --user

#settings a defined entry point
ENTRYPOINT [ "python", "data.py" ]
