import styles from './ResultList.module.css';

export default function ResultList({ results }) {
  return (
    <ul className={styles.resultList}>
      {results.map((result, index) => (
        <li key={index}>{result.name}</li> // Ajusta según la API
      ))}
    </ul>
  );
}
