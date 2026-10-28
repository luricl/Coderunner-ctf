# Coderunner-ctf target image
#
# Single container: Flask app (gunicorn) + sshd + the system users the
# privesc chain needs. Pinned so the image builds reproducibly.
FROM python:3.12.7-slim-bookworm

# openssh-server + sudo: SSH access for martin and the sudo rule issue #16
# wires up. gosu: lets root (needed for sshd) drop to app-production to run
# gunicorn, without a SUID binary. No other packages — nothing here should
# open an unintended privesc path (issue #19).
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        openssh-server=1:9.2p1-2+deb12u10 \
        sudo=1.9.13p3-1+deb12u4 \
        gosu=1.14-1+b10 \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /run/sshd \
    && ssh-keygen -A

# Low-priv web user. No shell/SSH login — gunicorn runs as this user, it has
# no business reaching the box interactively.
RUN useradd --system --create-home --home-dir /home/app-production \
        --shell /usr/sbin/nologin app-production

# Interactive SSH user for the privesc chain.
RUN useradd --create-home --home-dir /home/martin \
        --shell /bin/bash martin \
    && passwd -l martin

WORKDIR /opt/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chown -R app-production:app-production /opt/app

EXPOSE 5000 22

CMD ["gosu", "app-production", "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
