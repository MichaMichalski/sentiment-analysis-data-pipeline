import psycopg2

# dbname should be the same for the notifying process
conn = psycopg2.connect(host="mypg", dbname="twittereloncrypto", user="postgres", password=1234)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cursor = conn.cursor()
cursor.execute("DROP TRIGGER IF EXISTS add_task_event_trigger ON tweets")
conn.commit()
cursor.execute(
    """
    CREATE OR REPLACE FUNCTION add_task_notify()
    RETURNS trigger AS
    $BODY$

    BEGIN
    PERFORM pg_notify('new_id', NEW.ID::text);
    RETURN NEW;
    END;
    $BODY$
    LANGUAGE plpgsql VOLATILE
    COST 100;
    ALTER FUNCTION add_task_notify()
    OWNER TO postgres;

    CREATE TRIGGER add_task_event_trigger
    AFTER INSERT
    ON tweets
    FOR EACH ROW
    EXECUTE PROCEDURE add_task_notify();
    """
)

conn.commit()