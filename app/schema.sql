
CREATE TABLE categories (
	id VARCHAR(50) NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	description TEXT, 
	icon VARCHAR(50), 
	color VARCHAR(50), 
	enabled BOOLEAN DEFAULT true, 
	CONSTRAINT categories_pkey PRIMARY KEY (id)
)



CREATE TABLE entries (
	id UUID NOT NULL, 
	date DATE NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	CONSTRAINT entries_pkey PRIMARY KEY (id)
)



CREATE TABLE metrics (
	id VARCHAR(50) NOT NULL, 
	category_id VARCHAR(50) NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	description TEXT, 
	unit VARCHAR(50) NOT NULL, 
	min_value NUMERIC, 
	max_value NUMERIC, 
	step_value NUMERIC, 
	default_value NUMERIC, 
	default_goal NUMERIC, 
	boolean_true_label VARCHAR(50), 
	boolean_false_label VARCHAR(50), 
	CONSTRAINT metrics_pkey PRIMARY KEY (id, category_id), 
	CONSTRAINT metrics_category_id_fkey FOREIGN KEY(category_id) REFERENCES categories (id) ON DELETE CASCADE
)



CREATE TABLE entry_metrics (
	entry_id UUID NOT NULL, 
	category_id VARCHAR(50) NOT NULL, 
	metric_id VARCHAR(50) NOT NULL, 
	value NUMERIC, 
	CONSTRAINT entry_metrics_pkey PRIMARY KEY (entry_id, category_id, metric_id), 
	CONSTRAINT entry_metrics_category_id_metric_id_fkey FOREIGN KEY(category_id, metric_id) REFERENCES metrics (category_id, id), 
	CONSTRAINT entry_metrics_entry_id_fkey FOREIGN KEY(entry_id) REFERENCES entries (id) ON DELETE CASCADE
)



CREATE TABLE goals (
	category_id VARCHAR(50) NOT NULL, 
	metric_id VARCHAR(50) NOT NULL, 
	value NUMERIC NOT NULL, 
	CONSTRAINT goals_pkey PRIMARY KEY (category_id, metric_id), 
	CONSTRAINT goals_category_id_metric_id_fkey FOREIGN KEY(category_id, metric_id) REFERENCES metrics (category_id, id)
)


